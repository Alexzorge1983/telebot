from aiogram import types, Dispatcher
from database import orm
from keyboards import inline
from settings.bot_config import bot, GROUP

post = []
answ = dict()
user = []
tg_psy_id = None

# Взять заявку по кнопке
# @dp.callback_query_handler(inquiries_cb.filter(action = 'accept'))
async def psy_inq(callback: types.CallbackQuery, callback_data: dict):
    res = callback.data
    the_dict = callback
    global tg_psy_id
    tg_psy_id = the_dict['from']['id']
    user_psy_name = the_dict['from']['username']
    user_psy_first_name = the_dict['from']['first_name']
    message_id = the_dict['message']['message_id']
    inq_id = int(the_dict['data'].split(":")[1])
    orm.create_psyhologi(tg_psy_id = tg_psy_id, user_psy_name=user_psy_name, user_psy_first_name=user_psy_first_name)
    if message_id not in post:
        post.append(message_id)
        orm.create_messages(message_id = message_id, inq_id = inq_id, tg_psy_id = tg_psy_id)
        inq =  orm.sql_read2(message_id = message_id)
        print(inq)
        tem = inq[0]
        inquiry = inq[1]
        tg_id = inq[2]
        user_name = inq[3]
        first_name = inq[4]
        await bot.send_message(tg_psy_id, f'ID пользователя: {tg_id}\nusername: @{user_name}\nИмя пользователя: {first_name}\nТема заявки: {tem}\nЗаявка: {inquiry}')
        await callback.message.delete()
        await callback.answer('Контакты отправлены вам в личные сообщения')
        await bot.send_message(GROUP, f'<b>Заявка взята в работу</b>\nТема заявки: {tem}\nЗаявка: {inquiry}',
                               parse_mode="html")
        # if f'{callback.from_user.id}' not in answ and len(user) == 0:
        #     answ[f'{callback.from_user.id}'] = res
        #     user.append(user_psy_id)
        #     await sqlite_db.sql_read2(message_id = message_id)
        #     await callback.answer('Контакты отправлены вам в личные сообщения')
        #     await sqlite_db.sql_read3(message_id=message_id)
        # else:
        #     await callback.answer('Заявка уже в работе', show_alert=True)
    else:
        await callback.answer('Что-то пошло не так!', show_alert=True)



# Версия 1 - проверка по номеру поста
#     if message_id not in post:
#         post.append(message_id)
#         await sqlite_db.create_messages(message_id = message_id,user_psy_id = user_psy_id, inq_id = inq_id)
#         await sqlite_db.sql_read2(message_id = message_id)
#         await callback.message.delete()
#         await callback.answer('Контакты отправлены вам в личные сообщения')
#         await sqlite_db.sql_read3(message_id=message_id)
#         # if f'{callback.from_user.id}' not in answ and len(user) == 0:
#         #     answ[f'{callback.from_user.id}'] = res
#         #     user.append(user_psy_id)
#         #     await sqlite_db.sql_read2(message_id = message_id)
#         #     await callback.answer('Контакты отправлены вам в личные сообщения')
#         #     await sqlite_db.sql_read3(message_id=message_id)
#         # else:
#         #     await callback.answer('Заявка уже в работе', show_alert=True)
#     else:
#         await callback.answer('Заявка уже в работе!', show_alert=True)
#     print(f'{post},{inq_id},{user},{answ},{callback}')


# Регистрируем психолога в боте
# @dp.register_message_handler(commands=['psy'])
# async def psy_reg(message: types.Message):
#     global PSY
#     PSY = message.from_user.id
#     await bot.send_message(message.from_user.id, 'Вы зарегистрированы и можете начать получать заявки')
#     await message.delete()

# # @dp.callback_query_handler(lambda callback: callback.data == 'psyh_inq_take')
# async def psy_inq88(callback: types.CallbackQuery):
#     res = callback.data
#     the_dict = callback
#     user_id = the_dict['from']['id']
#     first_name = the_dict['from']['first_name']
#     user_name = the_dict['from']['username']
#     if f'{callback.from_user.id}' not in answ:
#         answ[f'{callback.from_user.id}'] = res
#         await bot.send_message(chat_id=callback.message.chat.id, message = 'ваша заявка', parse_mode = 'html')
#         await callback.answer('Вы получили заявку в работу, она отправлена вам ботом в личные сообщения')
#     else:
#         await callback.answer('Заявка уже в работе', show_alert=True)
#     print(f'{callback}')


        # await bot.send_message(message.from_user.id, f'Вы взяли заявку в работу. Получите контакт клиента:\nИмя клиента: {first_name},\
        # \nID клиента: {user_id},\nusername: @{user_name}.\nПо возможности свяжитесь с ним в ближайшее время')




# @dp.message_handler()
# async def psyho_send(message: types.Message):
#     await sqlite_db.sql_read(message)


def register_handlers_psyholog(dp: Dispatcher):
    # dp.register_message_handler(publish_in_group)
    # dp.register_message_handler(psy_reg, commands=['psy'])
    dp.register_callback_query_handler(psy_inq,inline.inquiries_cb.filter(action = 'accept'))
    # dp.register_message_handler(psy_mes, content_types = ['text'])



# dp.register_callback_query_handler(psy_inq,lambda callback: callback.data == 'inq_id')
# Проблемы:
# вывод всех заявок сразу, должен брать только последнюю запись из бд в момент ее внесения / синхронизация
# в боте реагирует на команду старт
# к заявкам не должно быть доступа у пользователей бота, они анонимные
# просмотр заявок открыт для всех участников закрытой группы

# Психолог нажимает на кнопку "Взять заявку", после этого он получает инфо от кого заявка (user.id),
# одновременно с этим заявка становится недоступной для других (всплывает сообщение, что заявка
# уже в работе)

# 1/ Сообщение Заявка принята + вывод инфо о пользователе
# 2 / Блокировка заявки для всех с момента акцепта

# 2 состояния (условия) у кнопки - либо взята в работу, либо не взята


# 1. Если психолог брал 1 заявку в работу, то он может взять и еще одну заявку (массив заявок, +1 заявка)
# 2. Данные о заявке должны подгружаться у психолога в группе из БД:
# - текст заявки
# - после нажатия на кнопку данные клиента
# - все данные (текст + данные клиента пересылаются в личные от бота)



