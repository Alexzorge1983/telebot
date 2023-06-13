from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Zayavki, Mess, Psiho
from settings import database_config


engine = create_engine(database_config.url, client_encoding='utf8', echo = True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)



def create_user(tg_id, user_name, first_name):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id = tg_id, user_name = user_name, first_name = first_name)
        session.add(new_user)
        session.commit()

def create_zayavki(tg_id, tem, inquiry):
    session = Session()
    new_zayavka = Zayavki(tg_id = tg_id, tem = tem, inquiry = inquiry)
    session.add(new_zayavka)
    session.commit()

def get_zayavki():
    session = Session()
    q = session.query(Zayavki).order_by(desc(Zayavki.inq_id)).limit(1)
    for row in q:
        return row.inq_id
    session.commit()

def create_psyhologi(tg_psy_id, user_psy_name, user_psy_first_name):
    session = Session()
    user = session.query(Psiho).filter(Psiho.tg_psy_id == tg_psy_id).first()
    if user is None:
        new_user = Psiho(tg_psy_id = tg_psy_id, user_psy_name=user_psy_name, user_psy_first_name=user_psy_first_name)
        session.add(new_user)
        session.commit()

def create_messages(message_id, inq_id:int, tg_psy_id):
    session = Session()
    message = Mess(message_id = message_id, inq_id = inq_id, tg_psy_id = tg_psy_id)
    session.add(message)
    session.commit()

def sql_read2(message_id):
    session = Session()
    inq_m = session.query(Mess).filter(Mess.message_id == message_id).first()
    inq_id = inq_m.inq_id
    inq_z = session.query(Zayavki).filter(Zayavki.inq_id == inq_id).first()
    tg_id = inq_z.tg_id
    tem = inq_z.tem
    inquiry = inq_z.inquiry
    inq_u = session.query(User).filter(User.tg_id == tg_id).first()
    tg_id = inq_u.tg_id
    user_name = inq_u.user_name
    first_name = inq_u.first_name
    return tem, inquiry, tg_id, user_name, first_name

async def sql_read3(message_id):
    for ret in cur.execute("SELECT * FROM messages WHERE message_id ='{}'".format(message_id)):
        inq_id = ret[1]
        for ret_i in cur.execute("SELECT * FROM zayavki WHERE inq_id ='{}'".format(inq_id)):
            await bot.send_message(GROUP, f'<b>Заявка взята в работу</b>\nТема заявки: {ret_i[3]}\nЗаявка: {ret_i[4]}', parse_mode="html")
        base.commit()


# def create_report(tg_id, temp, feels_like, wind_speed, pressure_mm, city):
#     session = Session()
#     user = session.query(User).filter(User.tg_id == tg_id).first()
#     new_report = WeatherReport(owner = user.id, temp = temp, feels_like = feels_like, wind_speed = wind_speed, pressure_mm = pressure_mm, city = city)
#     session.add(new_report)
#     session.commit()
#
# def get_user_city(tg_id):
#     session = Session()
#     user = session.query(User).filter(User.tg_id == tg_id).first()
#     return user.city
#
# def get_reports(tg_id):
#     session = Session()
#     user = session.query(User).filter(User.tg_id == tg_id).first()
#     reports = user.reports
#     return reports
#
# def delete_user_report(report_id):
#     session = Session()
#     report = session.get(WeatherReport, report_id)
#     session.delete(report)
#     session.commit()
#
# def get_all_users():
#     session = Session()
#     users = session.query(User).all()
#     return users
