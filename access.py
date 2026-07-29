from app.services.google_sheets import GoogleSheetsRepository
class AccessService:
    def __init__(self, repository: GoogleSheetsRepository) -> None: self._repository=repository
    def is_allowed(self, user_id: int) -> bool:
        for row in self._repository.get_rows("users")[1:]:
            if len(row)>=3 and row[0].strip().isdigit() and int(row[0].strip())==user_id:
                return row[2].strip().upper()=="TRUE"
        return False
