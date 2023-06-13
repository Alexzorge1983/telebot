from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = '5686542241:AAE0cHBAcxTnj0liHemIDa-w6RYCDQWVdQE'
tg_bot_admin = [5688779987]
GROUP = '@psyhozaya'

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)