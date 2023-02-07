import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe


def main():
    # Get a Google Sheets client using a service account
    sheets_client = gspread.service_account("output/service_account.json")

    # Open the workbook
    workbook = sheets_client.open("Poe gem prices")

    # Read the CSV files into a Pandas DataFrame
    df1 = pd.read_csv("output/gems_to_corrupt.csv")
    df2 = pd.read_csv("output/gems_to_level.csv")

    # Update the worksheets with the values from the DataFrame
    set_with_dataframe(workbook.worksheet("Gems to corrupt"), df1)
    set_with_dataframe(workbook.worksheet("Gems to level"), df2)


if __name__ == "__main__":
    main()
