from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DateTime

engine = create_engine('mysql+pymysql://root:root@localhost/budget')
engine.connect()

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


class family(BaseModel):
    __tablename__ = 'family'

    id = Column(Integer, primary_key=True)
    firstname = Column(VARCHAR(30))
    lastname = Column(VARCHAR(30))
    role = Column(VARCHAR(30))
    age = Column(Integer)

    def __str__(self):
        return f"id       : {self.id}\n" \
               f"firstname: {self.firstname}\n" \
               f"lastname : {self.lastname}\n" \
               f"role     : {self.role}\n" \
               f"age      : {self.age}\n"


class costs(BaseModel):
    __tablename__ = 'costs'

    id = Column(Integer, primary_key=True)
    familyMemId = Column(Integer, ForeignKey(family.id))
    purpose = Column(VARCHAR(45))
    amount = Column(Integer)
    time = Column(DateTime)

    def __str__(self):
        return f"id         : {self.id}\n" \
               f"familyMemId: {self.familyMemId}\n" \
               f"purpose    : {self.purpose}\n" \
               f"amount     : {self.amount}\n" \
               f"time       : {self.time}\n"


class profits(BaseModel):
    __tablename__ = 'profits'

    id = Column(Integer, primary_key=True)
    familyMemId = Column(Integer, ForeignKey(family.id))
    amount = Column(Integer)
    time = Column(DateTime)

    def __str__(self):
        return f"id         : {self.id}\n" \
               f"familyMemId: {self.familyMemId}\n" \
               f"amount     : {self.amount}\n" \
               f"time       : {self.time}\n"