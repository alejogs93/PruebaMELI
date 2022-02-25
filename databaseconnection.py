from pymysql import OperationalError
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import logging

from models import Email, EmailList, MySqlConfig

Base = declarative_base()
logger1 = logging.getLogger('email_reader')

class Engine():
    def __init__(self, data:MySqlConfig):
        """"""
        self.__user = data.user
        self.__password = data.password
        self.__database = data.db
        self.__host = data.host
        self.__port = data.port
        self.__engine=""

        self.__create()

    def __create(self):
        url='mysql+pymysql://{}:{}@{}:{}/{}'.format(self.__user,self.__password,self.__host,self.__port,self.__database)
        print(url)
        self.__engine = create_engine(url, echo=True)
        Base.metadata.create_all(self.__engine)

    #Crear session de trabaj con base de datos con opcion de expiracion cuando se realice el commit
    def __create_session(self):
        session=""
        try:
            logger1.info('Creando Session')
            Session = sessionmaker(expire_on_commit=True)
            Session.configure(bind=self.__engine)
            session = Session()
        except Exception:
            logger1.critical('Error al crear session')
        return session
    
    def save_list_of_emails(self,e_list:EmailList):
        if len(e_list) >0 :
            logger1.info('Almacenando emails')
            try:
                session=self.__create_session()
                for email in e_list:
                    session.add(EmailEntity(e_from=email.e_from,subject=email.subject, date=email.date))
                session.commit()  
            except OperationalError:
                logger1.error('Error intentando almacenar el registro')
            except Exception:
                logger1.error('Error intentando almacenar el registro')
 
########################################################################
class EmailEntity(Base):
    """"""
    __tablename__ = "emails"
 
    id = Column(Integer, primary_key=True)
    e_from = Column(String(255))
    subject = Column(String(255))
    date = Column(Date())

    #----------------------------------------------------------------------
    def __init__(self, e_from, subject, date):
        """"""
        self.e_from = e_from
        self.subject = subject
        self.date = date

    def __repr__(self):
        return "<Email(from='{0}', subject='{1}', date='{2}')>".format(
                            self.e_from, self.subject, self.date)