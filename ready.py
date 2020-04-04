import sqlite3
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def init_system():
    database = sqlite3.connect('./City.db')
    engine = create_engine("sqlite:///City.db")
    Base = declarative_base()

    class City(Base):
        __tablename__ = 'City_num'
        name = Column(String(40), primary_key=True)
        id_number = Column(Integer)

    file = open("citycode.txt", 'r', encoding='UTF-8')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    namelist = []
    dirtydata = []
    for x in file.readlines():
        x = x.strip()
        if x:
            y, z = x.strip().split(',', 1)
        if y not in namelist:
            namelist.append(y)
            city = City(name=y, id_number=int(z))
            session.add(city)
        else:
            dirtydata.append((y, z))

    session.commit()
    session.close()
    database.close()
    file.close()
    print(dirtydata)
