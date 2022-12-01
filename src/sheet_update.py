import os
import gspread
import pandas as pd


def iter_pd(df):
    for val in df.columns:
        yield val
    for row in df.to_numpy():
        for val in row:
            if pd.isna(val):
                yield ""
            else:
                yield val


def pandas_to_sheets(pandas_df, sheet, clear=True):
    # Updates all values in a workbook to match a pandas dataframe
    if clear:
        sheet.clear()
    (row, col) = pandas_df.shape
    cells = sheet.range(
        "A1:{}".format(gspread.utils.rowcol_to_a1(row + 1, col))
    )
    for cell, val in zip(cells, iter_pd(pandas_df)):
        cell.value = val
    sheet.update_cells(cells)


def main():
    gc = gspread.service_account('/src/service_account')
    workbook = gc.open("Poe gem prices")
    df = pd.read_csv("output/gems.csv")
    pandas_to_sheets(df, workbook.worksheet("Poe gem prices"))


if __name__ == "__main__":
    main()
