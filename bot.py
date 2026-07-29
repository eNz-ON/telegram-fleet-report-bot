from __future__ import annotations
import asyncio, logging
from aiogram import Bot, Dispatcher
from app.config import Settings
from app.handlers.main import build_router
from app.scheduler import create_scheduler
from app.services.access import AccessService
from app.services.fleet import FleetService
from app.services.google_sheets import GoogleSheetsRepository
from app.services.reports import ReportService
async def main()->None:
    logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    settings=Settings.from_env()
    repo=GoogleSheetsRepository(settings.google_credentials_file,settings.google_sheet_key)
    access=AccessService(repo); fleet=FleetService(repo); reports=ReportService(repo)
    bot=Bot(settings.bot_token); dp=Dispatcher(); dp.include_router(build_router(access,fleet,reports))
    scheduler=create_scheduler(bot,settings,reports)
    if scheduler: scheduler.start()
    try: await dp.start_polling(bot)
    finally:
        if scheduler: scheduler.shutdown(wait=False)
        await bot.session.close()
if __name__=="__main__": asyncio.run(main())
