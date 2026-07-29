from __future__ import annotations
from collections.abc import Iterable
from pathlib import Path
import gspread
from gspread import Spreadsheet

class GoogleSheetsRepository:
    def __init__(self, credentials_file: Path, spreadsheet_key: str) -> None:
        self._credentials_file=credentials_file; self._spreadsheet_key=spreadsheet_key
    def _spreadsheet(self) -> Spreadsheet:
        return gspread.service_account(filename=str(self._credentials_file)).open_by_key(self._spreadsheet_key)
    def get_rows(self, worksheet_name: str) -> list[list[str]]:
        return self._spreadsheet().worksheet(worksheet_name).get_all_values()
    def find_existing_worksheet(self, possible_names: Iterable[str]) -> list[list[str]] | None:
        spreadsheet=self._spreadsheet()
        for name in possible_names:
            try: return spreadsheet.worksheet(name).get_all_values()
            except gspread.WorksheetNotFound: continue
        return None
