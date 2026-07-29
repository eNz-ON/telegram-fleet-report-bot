from __future__ import annotations
import asyncio
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.keyboards import main_keyboard, service_keyboard
from app.services.access import AccessService
from app.services.fleet import FleetService
from app.services.reports import ReportService
from app.states import SearchState

def build_router(access_service: AccessService, fleet_service: FleetService, report_service: ReportService) -> Router:
    router=Router()
    async def ensure_access(message: Message) -> bool:
        if message.from_user is None: return False
        allowed=await asyncio.to_thread(access_service.is_allowed,message.from_user.id)
        if not allowed: await message.answer("⛔ Brak dostępu")
        return allowed
    @router.message(CommandStart())
    async def start(message: Message,state:FSMContext)->None:
        if not await ensure_access(message): return
        await state.clear(); await message.answer("Cześć!",reply_markup=main_keyboard())
    @router.message(F.text=="📊 Raport")
    async def report(message:Message)->None:
        if not await ensure_access(message): return
        await message.answer(await asyncio.to_thread(report_service.build_report))
    @router.message(F.text=="👤 Kto jeździ")
    async def driver_search(message:Message,state:FSMContext)->None:
        if not await ensure_access(message): return
        await state.set_state(SearchState.waiting_for_driver_plate); await message.answer("Podaj numer rejestracyjny:")
    @router.message(F.text=="🚗 Flota")
    async def fleet_search(message:Message,state:FSMContext)->None:
        if not await ensure_access(message): return
        await state.set_state(SearchState.waiting_for_fleet_plate); await message.answer("Podaj numer rejestracyjny:")
    @router.message(F.text=="🔧 Serwis samochodów")
    async def service(message:Message)->None:
        if not await ensure_access(message): return
        await message.answer("Serwis:",reply_markup=service_keyboard())
    @router.message(SearchState.waiting_for_driver_plate)
    async def handle_driver(message:Message,state:FSMContext)->None:
        if not await ensure_access(message): return
        await message.answer((await asyncio.to_thread(fleet_service.find_driver,message.text or "")) or "❌ Nie znaleziono"); await state.clear()
    @router.message(SearchState.waiting_for_fleet_plate)
    async def handle_fleet(message:Message,state:FSMContext)->None:
        if not await ensure_access(message): return
        await message.answer((await asyncio.to_thread(fleet_service.find_vehicle,message.text or "")) or "❌ Nie znaleziono"); await state.clear()
    @router.message()
    async def fallback(message:Message)->None:
        if not await ensure_access(message): return
        await message.answer("Wybierz opcję 👇",reply_markup=main_keyboard())
    return router
