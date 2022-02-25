from dotenv import load_dotenv
import os, logging
from models import AppConfig, EmailConfig, MySqlConfig

load_dotenv(verbose=True)
logger1 = logging.getLogger('email_reader')

class Configuration():
    def __init__(self):
        self.__email_config = ""
        self.__db_config = ""
        self.__app_config = ""

        self.__init_configuration()

    def __init_configuration(self):
    #Crear objeto de configuracion basado en variables de entorno
        logger1.info('Leyendo variables de cuenta de email')

        email=os.getenv('EMAIL', 'default') #email cuenta usuario
        password=os.getenv('PASSWORD', 'default') #password correo
        connecton_type=os.getenv('CONNECTION_TYPE', 'gmail') #tipo de coneccion (gmail)
        mail_folder=os.getenv('MAIL_FOLDER', 'Inbox') #carpeta del buzon de correos (Inbox, Deleted)
        
        logger1.info('Leyendo variables de applicacion')

        loop_time=os.getenv('LOOP_TIME', 60) #tiempo de espera para revisar nuevos emails
        criteria=os.getenv('SEARCH_CRITERIA', 'BODY') #criterio de busqueda (BODY)
        keyword=os.getenv('SEARCH_KEYWORD', 'Risk') #palabra clave
        unseen=os.getenv('SEARCH_UNSEEN', 'True') #buscar en correos no leidos (True), correos leidos (False)
        
        logger1.info('Leyendo variables de base de datos')
        
        mysql_db=os.getenv('MYSQL_DB', 'email') 
        mysql_user=os.getenv('MYSQL_USER', 'root')
        mysql_pass=os.getenv('MYSQL_PASS', 'root')
        mysql_host=os.getenv('MYSQL_HOST', 'localhost')
        mysql_port=int(os.getenv('MYSQL_PORT', 3306))

        self.__db_config = MySqlConfig(db=mysql_db,host=mysql_host,port=mysql_port,
                                    user=mysql_user, password=mysql_pass)
        self.__email_config = EmailConfig(email=email,password=password,connection_type=connecton_type,
                            mail_folder=mail_folder)
        self.__app_config = AppConfig(loop_time=loop_time,criteria=criteria,keyword=keyword,
                            unseen=unseen)

    def get_bd_config(self) -> MySqlConfig:
        return self.__db_config

    def get_app_config(self) -> AppConfig:
        return self.__app_config

    def get_email_config(self) -> EmailConfig:
        return self.__email_config