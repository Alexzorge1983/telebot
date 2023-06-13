from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

inquiries_cb = CallbackData ('inquiry', 'id', 'action')

'''Inline Keyboards'''

firstkb = InlineKeyboardMarkup(row_width=1)
fButton2 = InlineKeyboardButton(text = 'Оставить запрос', callback_data = 'psyh_2')
fButton3 = InlineKeyboardButton(text = 'Подробнее о нас', callback_data = 'psyh3')
fButton4 = InlineKeyboardButton(text = 'Курсы по психологии', callback_data = 'psyh4')
fButton = InlineKeyboardButton(text = 'Для психологов', callback_data = 'psyh')

firstkb.add(fButton2, fButton3, fButton4,fButton)

agekb = InlineKeyboardMarkup(row_width=2)
aButton = InlineKeyboardButton(text = 'Да', callback_data = 'psyh_age_yes')
aButton2 = InlineKeyboardButton(text = 'Нет', callback_data = 'psyh_age_no')
agekb.add(aButton, aButton2)

temkb = InlineKeyboardMarkup(row_width=1)
tButton = InlineKeyboardButton(text = 'Депрессия', callback_data = 'psyh_t_depr')
tButton2 = InlineKeyboardButton(text = 'Проблемы в отношениях', callback_data = 'psyh_t_rel')
tButton3 = InlineKeyboardButton(text = 'Одиночество', callback_data = 'psyh_t_odin')
tButton4 = InlineKeyboardButton(text = 'Проблемы с самооценкой', callback_data = 'psyh_t_samo')
temkb.add(tButton, tButton2, tButton3, tButton4)


def get_inquiry_ikb(inq_id:int) -> InlineKeyboardMarkup:
    psykb = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = 'Взять заявку', callback_data = inquiries_cb.new(inq_id,'accept'))]

    ])
    return psykb

# psykb = InlineKeyboardMarkup(row_width=1)
# pButton = InlineKeyboardButton(text = 'Взять заявку', callback_data = 'inq_id')
# psykb.add(pButton)

# def pbutton(inq_id):
#     psykb = InlineKeyboardMarkup(row_width = 1).add(InlineKeyboardButton(text = 'Взять заявку', callback_data = f'{inq_id}'))
#     return psykb


