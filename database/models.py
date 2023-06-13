import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, select, Table, DateTime, BigInteger, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.orm import relationship



Base = declarative_base()

class User(Base):
    __tablename__ = 'PsyUsers'
    tg_id = Column(BigInteger, primary_key = True)
    user_name = Column(String, nullable = False)
    first_name = Column(String, nullable = False)
    inquiries = relationship('Zayavki', backref='inq', lazy = True, cascade = 'all, delete-orphan')

    def __repr__(self):
        return self.tg_id

class Zayavki(Base):
    __tablename__ = 'Inquiries'
    inq_id = Column(BigInteger, primary_key= True, nullable=False)
    inq_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    tg_id = Column(BigInteger, ForeignKey('PsyUsers.tg_id'), nullable = False)
    tem = Column(String, nullable=False)
    inquiry = Column(Text, nullable=False)
    message = relationship('Mess', back_populates = 'inq', uselist = False, lazy = True)

    def __repr__(self):
        return self.inq_id


class Mess(Base):
    __tablename__ = 'Messages'
    message_id = Column(BigInteger, primary_key= True)
    inq_id = Column(BigInteger, ForeignKey('Inquiries.inq_id'), nullable = False)
    tg_psy_id = Column(BigInteger, ForeignKey('Psihologi.tg_psy_id'), nullable = False)
    inq = relationship('Zayavki', back_populates='message', uselist=False, lazy=True)

    def __repr__(self):
        return self.message_id


class Psiho(Base):
    __tablename__ = 'Psihologi'
    tg_psy_id = Column(BigInteger, primary_key=True)
    user_psy_name = Column(String, nullable=False)
    user_psy_first_name = Column(String, nullable=False)
    messages = relationship('Mess', backref='mes', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.tg_psy_id