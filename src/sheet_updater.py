from pathlib import Path
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe


def main():
    # Get a Google Sheets client using a service account
    sheets_client = gspread.service_account(Path("output/service_account.json"))

    # Open the workbook
    workbook = sheets_client.open("Poe gem prices")

    df1 = pd.read_csv("output/gems_to_corrupt.csv")
    set_with_dataframe(workbook.worksheet("Gems to corrupt"), df1)

    df2 = pd.read_csv("output/gems_to_level.csv")
    set_with_dataframe(workbook.worksheet("Gems to level"), df2)

    df3 = pd.read_csv("output/currency_exchange.csv")
    set_with_dataframe(workbook.worksheet("Currency Flipping"), df3)


if __name__ == "__main__":
    main()
