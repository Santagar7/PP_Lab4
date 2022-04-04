from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DateTime, Float, Date
import datetime

engine = create_engine('mysql+pymysql://root:root@localhost/budget')
engine.connect()

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()
BaseModel.query = Session.query_property()


class Family(BaseModel):
    __tablename__ = 'family'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))

    def __init__(self, name, id=None):
        self.id = id
        self.name = name


class FamilyMembers(BaseModel):
    __tablename__ = 'family_members'

    id = Column(Integer, primary_key=True)
    login = Column(VARCHAR(50), unique=True)
    password = Column(VARCHAR(256))
    familyId = Column(Integer, ForeignKey(Family.id, onupdate="CASCADE", ondelete="CASCADE"))
    firstname = Column(VARCHAR(30))
    lastname = Column(VARCHAR(30))
    role = Column(VARCHAR(30))
    birthdate = Column(Date)

    def __init__(self, login, password, familyId, firstname=None, lastname=None, role=None, birthdate=None, id=None):
        self.id = id
        self.login = login
        self.password = password
        self.familyId = familyId
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.birthdate = birthdate


class Costs(BaseModel):
    __tablename__ = 'costs'

    id = Column(Integer, primary_key=True)
    familyMemId = Column(Integer, ForeignKey(FamilyMembers.id, onupdate="CASCADE", ondelete="CASCADE"))
    familyId = Column(Integer, ForeignKey(Family.id, onupdate="CASCADE", ondelete="CASCADE"))
    purpose = Column(VARCHAR(45))
    amount = Column(Float)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, purpose, amount, familyMemId=None, familyId=None, time=None, id=None):
        self.id = id
        self.familyMemId = familyMemId
        self.familyId = familyId
        self.purpose = purpose
        self.amount = amount
        self.time = time


class Profits(BaseModel):
    __tablename__ = 'profits'

    id = Column(Integer, primary_key=True)
    familyMemId = Column(Integer, ForeignKey(FamilyMembers.id, onupdate="CASCADE", ondelete="CASCADE"))
    familyId = Column(Integer, ForeignKey(Family.id, onupdate="CASCADE", ondelete="CASCADE"))
    amount = Column(Float)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, familyMemId, familyId, amount, time=None, id=id):
        self.familyMemId = familyMemId
        self.familyId = familyId
        self.amount = amount
        self.time = time


BaseModel.metadata.create_all(engine)
