from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    google_sheet_key: str
    google_credentials_file: Path
    report_chat_id: int | None
    timezone: str
    report_weekday: str
    report_hour: int
    report_minute: int

    @classmethod
    def from_env(cls) -> "Settings":
        bot_token=os.getenv("BOT_TOKEN","").strip()
        sheet_key=os.getenv("GOOGLE_SHEET_KEY","").strip()
        credentials=Path(os.getenv("GOOGLE_CREDENTIALS_FILE","service_account.json"))
        if not bot_token: raise RuntimeError("BOT_TOKEN is not configured.")
        if not sheet_key: raise RuntimeError("GOOGLE_SHEET_KEY is not configured.")
        if not credentials.exists(): raise RuntimeError(f"Google credentials file was not found: {credentials}")
        raw_chat_id=os.getenv("REPORT_CHAT_ID","").strip()
        return cls(bot_token, sheet_key, credentials, int(raw_chat_id) if raw_chat_id else None,
                   os.getenv("TIMEZONE","Europe/Warsaw"), os.getenv("REPORT_WEEKDAY","tue"),
                   int(os.getenv("REPORT_HOUR","10")), int(os.getenv("REPORT_MINUTE","0")))
