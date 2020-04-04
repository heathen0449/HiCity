from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///City.db")
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()


class CityList(Base):
    __tablename__ = 'City_num'
    name = Column(String(80), primary_key=True)
    id_number = Column(Integer)


def add_list(name, number):
    face = session.query(CityList).filter_by(name=name).fist()
    if face:
        print("你输入的城市已经存在")
        change_list(name, number)
    else:
        session.add(CityList(name=name, id_number=number))
        session.commit()
        print("信息已成功添加")


def change_list(name, number):
    face = session.query(CityList).filter_by(name=name).first()
    if face is None:
        print("您输入的城市并不存在")
        return
    else:
        face.number = number
        session.commit()


def del_list(name):
    face = session.query(CityList).filter_by(name=name).first()
    if face is None:
        print("您输入的城市名字并不存在")
    else:
        session.query(CityList).filter_by(name=name).delete()


def find_name(number):
    s = session.query(CityList).filter_by(id_number=number).first().name
    if s:
        return s
    else:
        print('输入错误')
        return


def find_number(name):
    s = session.query(CityList).filter_by(name=name).first().id_number
    if s:
        return s
    else:
        print('输入错误')
        return


