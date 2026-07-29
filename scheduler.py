from __future__ import annotations
import asyncio, logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import Settings
from app.services.reports import ReportService
logger=logging.getLogger(__name__)
def create_scheduler(bot:Bot,settings:Settings,report_service:ReportService)->AsyncIOScheduler|None:
    if settings.report_chat_id is None:
        logger.info("REPORT_CHAT_ID is not configured; scheduled reports are disabled."); return None
    scheduler=AsyncIOScheduler(timezone=settings.timezone)
    async def send_report()->None:
        await bot.send_message(settings.report_chat_id,await asyncio.to_thread(report_service.build_report))
    scheduler.add_job(send_report,"cron",day_of_week=settings.report_weekday,hour=settings.report_hour,minute=settings.report_minute,id="weekly_fleet_report",replace_existing=True)
    return scheduler
