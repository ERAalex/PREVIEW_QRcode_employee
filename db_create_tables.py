import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

######## Изменить перед отправкой в Docker

# engine = create_engine('')
engine = create_engine('')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40))
    surname = sq.Column(sq.String(length=40))
    email = sq.Column(sq.String(length=40), unique=True)
    position = sq.Column(sq.String(length=40))
    telephone = sq.Column(sq.String(length=12), unique=True)
    foto = sq.Column(sq.String)
    status = sq.Column(sq.Boolean)


class Qr_foto_table(Base):
    __tablename__ = 'qr_foto_table'

    id = sq.Column(sq.Integer, primary_key=True)
    qr_foto = sq.Column(sq.String)
    id_employee = sq.Column(sq.Integer, sq.ForeignKey('employee.id'), nullable=False)

    employee = relationship(Employee, backref='qr_foto_tables')


    def __str__(self):
        return f'{self.id}'


# def create_table(engine):
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#
# create_table(engine)