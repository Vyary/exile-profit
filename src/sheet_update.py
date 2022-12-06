import gspread
import pandas as pd


def pandas_to_sheets(
    pandas_df: pd.DataFrame, sheet: gspread.Worksheet, clear: bool = True
) -> None:
    """
    Updates all values in a worksheet to match a Pandas DataFrame.
    """
    # Clear the worksheet if specified
    if clear:
        sheet.clear()

    # Update the worksheet with the values from the DataFrame
    sheet.update([pandas_df.columns.tolist()] + pandas_df.values.tolist())


def main():
    # Get a Google Sheets client using a service account
    sheets_client = gspread.service_account("output/service_account.json")  # type: ignore

    # Open the workbook
    workbook = sheets_client.open("Poe gem prices")

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv("output/gems.csv")

    # Update the worksheet with the values from the DataFrame
    pandas_to_sheets(df, workbook.worksheet("Poe gem prices"))


if __name__ == "__main__":
    main()
