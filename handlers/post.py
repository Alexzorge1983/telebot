from aiogram import types, Dispatcher
from settings.bot_config import dp, bot, GROUP
from database import sqlite_db as sq

inq_id = None
post = []


# @dp.message_handler(content_types = ['text'])
# async def send_inquiry(message :types.Message):
#   await sqlite_db.sql_read()
#     for ret in sq.sql_read():
#         global inq_id
#         inq_id = ret[0]
#         await bot.send_message(GROUP, f'\nТема заявки: {ret[3]}\nЗаявка: {ret[4]}', reply_markup=inline.psykb)



# # @dp.message_handler(chat_id=GROUP)
# async def posting(message: types.Message):
#     print(message.text)
#     message_id = message.message_id
#     if message_id not in post:
#         post.append(message_id)
#         # await sqlite_db.update_zayavki(message_id=message_id)
#     else:
#         pass
#     print(f'{message_id},{post}')


# def register_handlers_posts(dp: Dispatcher):
#     dp.register_message_handler(send_inquiry, content_types = ['text'])