import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe


def main():
    # Get a Google Sheets client using a service account
    sheets_client = gspread.service_account("output/service_account.json")  # type: ignore

    # Open the workbook
    workbook = sheets_client.open("Poe gem prices")

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv("output/gems.csv")

    # Update the worksheet with the values from the DataFrame
    set_with_dataframe(workbook.worksheet("Poe gem prices"), df)

if __name__ == "__main__":
    main()
