from aiogram.fsm.state import State, StatesGroup

class SearchState(StatesGroup):
    waiting_for_driver_plate = State()
    waiting_for_fleet_plate = State()
