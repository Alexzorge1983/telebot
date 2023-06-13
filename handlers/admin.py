from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from settings.bot_config import dp, bot, GROUP
from database import sqlite_db
from keyboards import admin_kb

class FSMAdmin(StatesGroup):
    psy_add = State()
    psy_del = State()
    psy_username = State()
    psy_name = State()

'''Admin Message Handlers'''

# Текстовый блок (вынесьти отдельно в messages)
greeting_text_0 =  "Что хозяин надо?"

# Запуск бота в работу, приветственное сообщение
# @dp.message_handler(commands=['admin'])
async def command_admin(message :types.Message):
    await bot.send_message(message.from_user.id, greeting_text_0, reply_markup=admin_kb.button_case_admin)

# @dp.message_handler(commands = ['Добавить'], state=None)
async def psy_add(message : types.Message):
        await FSMAdmin.psy_add.set()
        await message.reply('Введи ID психолога')

# @dp.message_handler(commands = ['Удалить'], state=None)
async def psy_delete(message : types.Message):
        await FSMAdmin.psy_del.set()
        await message.reply('Введи username психолога')

# @dp.message_handler(commands = ['Получить_список'], state=None)
async def psy_get(message : types.Message):
        await FSMAdmin.psy_get.set()
        await message.reply('Введи username психолога')

# @dp.message_handler(content_types = ['text'], state=FSMAdmin.psy_add)
async def load_psy_id(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['psy_add'] = message.text
        await FSMAdmin.psy_username.set()
        await message.reply('Теперь введи username')

# @dp.message_handler(content_types = ['text'], state=FSMAdmin.psy_del)
async def del_psy_username(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['psy_del'] = message.text
        psy_del = message.text
        await sqlite_db.delete_psyhologi(user_psy_name = psy_del)
        await message.reply(f'Психолог с username {psy_del} из базы удален')
        await state.finish()

# @dp.message_handler(content_types = ['text'], state=FSMAdmin.psy_get)
async def get_psy_username(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['psy_get'] = message.text
        psy_del = message.text
        await sqlite_db.get_psyhologi(user_psy_name = psy_del)
        await message.reply('Получите актуальный список психологов')
        await state.finish()

# @dp.message_handler(content_types = ['text'], state=FSMAdmin.psy_username)
async def load_psy_username(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['psy_username'] = message.text
        await FSMAdmin.psy_name.set()
        await message.reply('Теперь введи имя психолога')

# @dp.message_handler(content_types = ['text'], state=FSMAdmin.psy_name)
async def load_psy_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['psy_name'] = message.text
        user_psy_id = data.get('psy_add')
        user_psy_name = data.get('psy_username')
        user_psy_first_name = message.text
        await sqlite_db.create_psyhologi2(user_psy_id = user_psy_id, user_psy_name = user_psy_name, user_psy_first_name = user_psy_first_name)
        await message.reply(f'Получили данные {user_psy_id},{user_psy_name},{user_psy_first_name}')
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_admin, commands=['admin'])
    dp.register_message_handler(psy_add, commands = ['Добавить'], state=None)
    dp.register_message_handler(psy_delete, commands = ['Удалить'], state=None)
    dp.register_message_handler(load_psy_id, content_types = ['text'], state=FSMAdmin.psy_add)
    dp.register_message_handler(del_psy_username, content_types = ['text'], state=FSMAdmin.psy_del)
    dp.register_message_handler(load_psy_username, content_types = ['text'], state=FSMAdmin.psy_username)
    dp.register_message_handler(load_psy_name, content_types = ['text'], state=FSMAdmin.psy_name)