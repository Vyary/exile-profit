from pathlib import Path

import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe


class GoogleSheetsClient:
    def __init__(self, credentials_file_path: str):
        self.client = gspread.service_account(Path(credentials_file_path))

    def open_workbook(self, name: str):
        return self.client.open(name)


class Workbook:
    def __init__(self, name: str, sheets_client: GoogleSheetsClient):
        self.name = name
        self.sheets_client = sheets_client
        self.workbook = self.sheets_client.open_workbook(name)

    def set_dataframe(self, sheet_name: str, dataframe: pd.DataFrame):
        worksheet = self.workbook.worksheet(sheet_name)
        set_with_dataframe(worksheet, dataframe)


class SheetUpdater:
    def __init__(self, credentials_file_path: str, workbook_name: str):
        self.google_sheets_client = GoogleSheetsClient(credentials_file_path)
        self.workbook = Workbook(workbook_name, self.google_sheets_client)

    def update(self, sheet_name: str, data_file: str):
        data = pd.read_csv(data_file, encoding="ISO-8859-1")
        self.workbook.set_dataframe(sheet_name, data)
