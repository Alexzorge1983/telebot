import sqlite3 as sq
from datetime import date
from settings.bot_config import bot, GROUP
from keyboards import *
from handlers import psyholog

current_date = date.today()
print(current_date)
inq_id = None

def sql_start():
    global base, cur
    base = sq.connect('psyhozay.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, user_name TEXT, first_name TEXT)')

    base.execute('CREATE TABLE IF NOT EXISTS zayavki (inq_id INTEGER PRIMARY KEY, DateTime DATE, user_id TEXT, tem TEXT, inquiry TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id))')

    base.execute('CREATE TABLE IF NOT EXISTS messages (message_id INT PRIMARY KEY, inq_id INTEGER, user_psy_id TEXT, FOREIGN KEY (inq_id) REFERENCES zayavki (inq_id), FOREIGN KEY (user_psy_id) REFERENCES psyhologi (user_psy_id) ON DELETE CASCADE)')

    base.execute('CREATE TABLE IF NOT EXISTS psyhologi (user_psy_id TEXT PRIMARY KEY, user_psy_name TEXT, user_psy_first_name TEXT)')

    base.commit()

async def create_user(user_id, user_name,first_name):
    cur.execute("SELECT user_id FROM users WHERE user_id ='{}'".format(user_id))
    rez = cur.fetchall()
    print (f'{rez}')
    if not rez:
        cur.execute('INSERT INTO users (user_id, user_name, first_name) VALUES (?,?,?)', (user_id, user_name, first_name))
        print('Добавил в базу юзеров')
    else:
        print('Уже в базе юзеров')
    base.commit()

async def create_zayavki(user_id, tem, inquiry):
    cur.execute('INSERT INTO zayavki (DateTime, user_id, tem, inquiry) VALUES (?,?,?,?)', (current_date, user_id, tem, inquiry))
    base.commit()

async def create_messages(message_id, inq_id:int, user_psy_id):
    cur.execute('INSERT INTO messages (message_id, inq_id, user_psy_id) VALUES (?,?,?)',(message_id, inq_id, user_psy_id))
    base.commit()

async def create_psyhologi(user_psy_id, user_psy_name, user_psy_first_name):
    cur.execute("SELECT user_psy_id FROM psyhologi WHERE user_psy_id ='{}'".format(user_psy_id))
    rez_p = cur.fetchall()
    print (f'{rez_p}')
    if not rez_p:
        cur.execute('INSERT INTO psyhologi (user_psy_id, user_psy_name, user_psy_first_name) VALUES (?,?,?)',(user_psy_id, user_psy_name, user_psy_first_name))
        print('Добавил в базу психологов')
    else:
        print('Уже в базе психологов')
        base.commit()

async def create_psyhologi2(user_psy_id, user_psy_name, user_psy_first_name):
    cur.execute("SELECT user_psy_id FROM psyhologi WHERE user_psy_id ='{}'".format(user_psy_id))
    rez_p = cur.fetchall()
    print (f'{rez_p}')
    if not rez_p:
        cur.execute('INSERT INTO psyhologi (user_psy_id, user_psy_name, user_psy_first_name) VALUES (?,?,?)',(user_psy_id, user_psy_name, user_psy_first_name))
        print('Добавил в базу психологов')
    else:
        print('Уже в базе психологов')
        base.commit()

async def delete_psyhologi(user_psy_name):
    cur.execute("SELECT user_psy_name FROM psyhologi WHERE user_psy_name ='{}'".format(user_psy_name))
    rez_p = cur.fetchall()
    print (f'{rez_p}')
    if rez_p:
        cur.execute("DELETE from psyhologi WHERE user_psy_name ='{}'".format(user_psy_name))
        print('Удалил из базы психологов')
    else:
        print('Нет в базе психологов')
        base.commit()


async def sql_read():
    for ret in cur.execute("SELECT * FROM zayavki ORDER by inq_id DESC LIMIT 1"):
        await bot.send_message(GROUP, f'Тема заявки: {ret[3]}\nЗаявка: {ret[4]}', reply_markup= inline.get_inquiry_ikb(ret[0]))
        base.commit()

async def sql_read2(message_id):
    for ret in cur.execute("SELECT * FROM messages WHERE message_id ='{}'".format(message_id)):
        inq_id = ret[1]
        for ret_i in cur.execute("SELECT * FROM zayavki WHERE inq_id ='{}'".format(inq_id)):
            user_id = ret_i[2]
            for ret_u in cur.execute("SELECT * FROM users WHERE user_id ='{}'".format(user_id)):
                await bot.send_message(psyholog.user_psy_id, f'ID пользователя: {ret_u[0]}\nusername: @{ret_u[1]}\nИмя пользователя: {ret_u[2]}\nТема заявки: {ret_i[3]}\nЗаявка: {ret_i[4]}')
        base.commit()

async def sql_read3(message_id):
    for ret in cur.execute("SELECT * FROM messages WHERE message_id ='{}'".format(message_id)):
        inq_id = ret[1]
        for ret_i in cur.execute("SELECT * FROM zayavki WHERE inq_id ='{}'".format(inq_id)):
            await bot.send_message(GROUP, f'<b>Заявка взята в работу</b>\nТема заявки: {ret_i[3]}\nЗаявка: {ret_i[4]}', parse_mode="html")
        base.commit()

async def sql_read4():
    cur.execute("SELECT user_psy_id FROM psyhologi").fetchall()
    base.commit()






# async def update_zayavki(message_id:int):
#     cur.execute('INSERT INTO zayavki (message_id) VALUES (?)',(message_id,))
#     base.commit()


# async def update_zayavki(tem, inquiry, user_id):
#         cur.execute("UPDATE zayavki SET tem = '{}', inquiry = '{}' WHERE user_id = '{}' AND ROWID IN ( SELECT max( ROWID ) FROM zayavki )".format(tem, inquiry, user_id))
#         base.commit()

# async def update_profile2(user_id, message_id, user_psy_id, user_psy_name, user_psy_first_name, inquiry):
#         cur.execute("UPDATE zayavki SET message_id = '{}', user_psy_id = '{}', user_psy_name = '{}', user_psy_first_name = '{}' WHERE user_id = '{}' AND inquiry = '{}'".format(message_id, user_psy_id, user_psy_name, user_psy_first_name, user_id, inquiry))
#         base.commit()


# callback.message.chat.id,
# ('SELECT * FROM zayavki').fetchall():
# ('SELECT * from zayavki ORDER by inq_id DESC limit 1').fetchone():
# SELECT last_insert_rowid()

# async def sql_add_command(state):
#     async with state.proxy() as data:
#         cur.execute('INSERT INTO zayavki VALUES (?,?)', tuple(data.values()))


# async def sql_read(message):
#     for ret in cur.execute('SELECT * FROM zayavki').fetchall():
#         await bot.send_message(GROUP, f'Тема заявки:{ret[0]}\nЗаявка:{ret[1]}')

#
# async def sql_read2(message):
#     return cur.execute('SELECT * FROM zayavki').fetchall()
#
# async def sql_delete_command(data):
#     cur.execute('SELECT FROM zayavki WHERE name == ?', (data,))
#     base.commit()