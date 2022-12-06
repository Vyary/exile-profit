import gspread
import pandas as pd


def iter_pd(df: pd.DataFrame):
    """
    Yields the values of a Pandas DataFrame, handling missing values.
    """
    for val in df.columns:
        yield val
    for row in df.to_numpy():
        for val in row:
            if pd.isna(val):
                yield ""
            else:
                yield val


def pandas_to_sheets(
    pandas_df: pd.DataFrame, sheet: gspread.Worksheet, clear: bool = True
) -> None:
    """
    Updates all values in a worksheet to match a Pandas DataFrame.
    """
    # Clear the worksheet if specified
    if clear:
        sheet.clear()

    # Get the shape of the DataFrame
    (row_count, col_count) = pandas_df.shape

    # Calculate the end cell of the worksheet range
    end_cell = gspread.utils.rowcol_to_a1(row_count + 1, col_count)

    # Get the cells in the worksheet range
    cells = sheet.range("A1:{}".format(end_cell))

    # Update the cell values with the values from the DataFrame
    for cell, val in zip(cells, iter_pd(pandas_df)):
        cell.value = val

    # Update the worksheet with the new cell values
    sheet.update_cells(cells)


def main():
    # Get a Google Sheets client using a service account
    sheets_client = gspread.service_account("output/service_account.json")

    # Open the workbook
    workbook = sheets_client.open("Poe gem prices")

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv("output/gems.csv")

    # Update the worksheet with the values from the DataFrame
    pandas_to_sheets(df, workbook.worksheet("Poe gem prices"))


if __name__ == "__main__":
    main()
