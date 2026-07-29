from __future__ import annotations
from collections import Counter
from datetime import datetime
from app.services.google_sheets import GoogleSheetsRepository
class ReportService:
    REPORT_SHEETS={"CITI":"🚗 Samochody kurierskie","Toyoty":"🚖 Samochody taxi","rowery":"🚲 Rowery","skutery":"🛵 Skutery"}
    def __init__(self, repository: GoogleSheetsRepository) -> None: self._repository=repository
    def build_report(self) -> str:
        result=[f"📊 Raport — {datetime.now():%d.%m.%Y}",""]; total=Counter()
        for sheet_name,title in self.REPORT_SHEETS.items():
            counts=Counter()
            for row in self._repository.get_rows(sheet_name)[1:]:
                if len(row)>5:
                    status=self._normalize_status(row[5])
                    if status: counts[status]+=1
            result.append(title)
            if counts:
                for status,count in sorted(counts.items()): result.append(f"• {status}: {count}"); total[status]+=count
            else: result.append("• Brak danych")
            result.append("")
        result.append("📌 RAZEM")
        if total:
            for status,count in sorted(total.items()): result.append(f"• {status}: {count}")
        else: result.append("• Brak danych")
        return "\n".join(result)
    @staticmethod
    def _normalize_status(value: str) -> str | None:
        normalized=value.strip().lower()
        return None if not normalized or normalized=="zakończony" else normalized.capitalize()
