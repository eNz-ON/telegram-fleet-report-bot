# Telegram Fleet Report Bot

A Telegram bot for internal fleet operations. It reads operational data from Google Sheets, generates fleet status reports, and lets authorized users look up vehicle and driver information directly in Telegram.

> Portfolio version: secrets, credentials, company data, and production identifiers are intentionally excluded.

## Features
- Consolidated fleet status reports from multiple worksheets
- Driver lookup by registration plate
- Vehicle, insurance, and company information lookup
- Google Sheets based access control
- Optional scheduled reports with APScheduler
- Reply and inline keyboard navigation

## Architecture
```text
Telegram user -> aiogram handlers -> services -> Google Sheets
```

## Stack
Python 3.11+, aiogram 3, gspread, Google Sheets API, APScheduler, python-dotenv

## Project structure
```text
app/handlers      Telegram handlers
app/services      Business logic and Google Sheets access
app/config.py     Environment configuration
app/scheduler.py  Optional scheduled report
bot.py            Application entry point
```

## Google Sheets
Expected worksheets: `CITI`, `Toyoty`, `rowery`, `skutery`, `flota`, a company sheet (`spółki`/variants), and `users`.

`users` format:
```text
telegram_id | role  | active
123456789   | admin | TRUE
```

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python bot.py
```

On Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python bot.py
```

## Security
Never commit Telegram tokens, spreadsheet IDs, service-account JSON files, production exports, or real customer/company data.

## License
MIT
