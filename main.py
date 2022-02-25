import os, logging, time
import customlogging
from configurator import Configuration
from emailconnection import EmailConnection
from databaseconnection import Engine

logger1 = logging.getLogger('email_reader')

#Objeto global para almacenar la instancia de coneccion y actulizar en caso de falla sin interrumpir el ciclo infinito del Daemon
EMAIL_CONNECTION = ""

#Ciclo infinito para revisar el buzon de email en busca de mensajes que cumplan el criterio de busqueda
def endless_loop(config:Configuration, engine: Engine):
    logger1.info('Iniciando proceso....')
    appconfig=config.get_app_config()
    while True:
        try:
            if appconfig.criteria == 'BODY':
                result = EMAIL_CONNECTION.search_email_matching_body_condition(appconfig.keyword,appconfig.unseen)      
                engine.save_list_of_emails(result)
        except Exception:
            logging.error('Error durante el proceso')
            establish_connection(config)
        logger1.info('Durmiendo....')
        time.sleep(int(appconfig.loop_time))

#Establecer conneccion con el servidor IMAP
def establish_connection(config:Configuration):
    global EMAIL_CONNECTION
    EMAIL_CONNECTION = EmailConnection(config.get_email_config())
    EMAIL_CONNECTION.connect()

def create_db_engine(config:Configuration):
    return Engine(config.get_bd_config())

def main():
    #obtener la configuracion desde las variables de entorno
    config = Configuration()
    #establecer conneccion con el servidor imap de acuerdo a la configuracion
    establish_connection(config)
    #crear motor de coneccion con base de datos
    engine = create_db_engine(config)
    #iniciar daemon
    endless_loop(config, engine)


if __name__ == "__main__":
    main()