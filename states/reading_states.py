# states/reading_states.py
from aiogram.fsm.state import State, StatesGroup

class ReadingWebsite(StatesGroup):
    reading = State()