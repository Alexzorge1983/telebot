from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from database import orm
from keyboards import inline
from settings.bot_config import bot, GROUP, dp

user_id = None
inquiry = None

class FSMClient(StatesGroup):
    tem = State()
    inquiry = State()


'''Message Handlers'''

# Текстовый блок (вынесьти отдельно в messages)
greeting_text_0 =  "Приветствуем вас в нашем боте! Пожалуйста, выберите подходящий вариант. Вы психолог или \
вы хотели бы оставить заявку?"
greeting_text_1 = "Ответьте на вопрос: Вам уже есть 18 лет?"
greeting_text_2 = "Выберите подходящую для вас тему"
greeting_text_3 = "Спасибо за ответы. Вы можете оставить заявку обратным сообщением и психолог напишет \
вам в ближайшее время в личных собщениях. По условиям бота первая консультация бесплатная"



# Запуск бота в работу, приветственное сообщение
# @dp.message_handler(commands=['start','help'])
async def command_start(message :types.Message):
    orm.create_user(tg_id=message.from_user.id, user_name=message.from_user.username, first_name=message.from_user.first_name)
    # user_id = message.from_user.id
    # first_name = message.from_user.first_name
    # user_name = message.from_user.username
    await bot.send_message(message.from_user.id, greeting_text_0, reply_markup=inline.firstkb)


# @bot.callback_query_handler(lambda callback: callback.data == 'psyh_2')
async def client_answer(callback_query: types.CallbackQuery):
    await callback_query.message.answer(greeting_text_1, reply_markup=inline.agekb)
    await callback_query.answer()

# @bot.callback_query_handler(lambda callback: callback.data == 'psyh')
async def psyho_answer(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Принимаются заявки о сотрудничестве. Напишите админу для получения более подробной информации - ')
    await callback_query.answer()

# @bot.callback_query_handler(lambda callback: callback.data in ['psyh_age_yes', 'psyh_age_no'])
async def age_answer(callback_query: types.CallbackQuery):
    if callback_query.data == 'psyh_age_no':
        await callback_query.message.answer('Извините, но с подростками не работаем. Вы можете обратиться на горячую линию:')
        await callback_query.answer()
    else:
        await callback_query.message.answer(greeting_text_2, reply_markup=inline.temkb)
        await callback_query.answer()
        await FSMClient.tem.set()

# @bot.callback_query_handler(lambda callback: callback.data in ['psyh_t_depr', 'psyh_t_rel', 'psyh_t_odin', 'psyh_t_samo'], state=FSMClient.tem)
async def tem_answer(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
         data['tem'] = callback_query.data
    dict_psyh = {"psyh_t_depr": "Депрессия", "psyh_t_rel": "Отношения", "psyh_t_odin": "Одиночество", "psyh_t_samo": "Самооценка"}
    tem = dict_psyh[callback_query.data]
    await callback_query.message.answer(greeting_text_3)
    await callback_query.answer()
    await state.update_data(tem=tem)
    await FSMClient.inquiry.set()

# @dp.message_handler(content_types = ['text'], state=FSMClient.inquiry)
async def write_inquiry(message :types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['inquiry'] = message.text
    global inquiry
    inquiry = message.text
    tem = data.get('tem')
    # user_id = message.from_user.id
    # first_name = message.from_user.first_name
    # user_name = message.from_user.username
    global user_id
    user_id = message.from_user.id
    user_name = message.from_user.username
    if not user_name:
        # await bot.forward_message(GROUP, message.chat.id, message_id=message.message_id)
        await bot.send_message(message.from_user.id, 'К сожалению, мы не можем принять вашу заявку, так как у вас не установлен в аккаунте username, поэтому психолог не сможет с вами связаться. Установите, пожалуйста, username и повторите процесс подачи заявки, нажав на команду /start')
    else:
        orm.create_zayavki(tg_id = message.from_user.id, tem = tem, inquiry = inquiry)
        inq_id = orm.get_zayavki()
        await bot.send_message(GROUP, f'Тема заявки: {tem}\nЗаявка: {inquiry}', reply_markup=inline.get_inquiry_ikb(inq_id))
        await bot.send_message(message.from_user.id,'Ваша заявка принята! Скоро с вами свяжется специалист, ожидайте')
        print(f'Тема заявки:{tem}\n Заявка: {inquiry}\n')
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_callback_query_handler(client_answer, lambda callback: callback.data == 'psyh_2')
    dp.register_callback_query_handler(psyho_answer, lambda callback: callback.data == 'psyh')
    dp.register_callback_query_handler(age_answer, lambda callback: callback.data in ['psyh_age_yes', 'psyh_age_no'])
    dp.register_callback_query_handler(tem_answer, lambda callback: callback.data in ['psyh_t_depr', 'psyh_t_rel', 'psyh_t_odin', 'psyh_t_samo'], state= FSMClient.tem)
    dp.register_message_handler(write_inquiry, content_types = ['text'], state=FSMClient.inquiry)
