import imaplib, email, logging, traceback, time, sys, datetime
from models import Email, EmailConfig, EmailList
from dateutil import parser

logger1 = logging.getLogger('email_reader')

class EmailConnection:
    def __init__(self, data:EmailConfig):
        self.__user = data.email
        self.__password = data.password
        self.__conn_type = data.connection_type
        self.__source = data.mail_folder
        self.__connection=""
        self.__connected=False

    def connect(self) -> bool:
        imap_url=''
        if self.__conn_type == 'gmail':
            imap_url = 'imap.gmail.com'

        logger1.info('Intentando establecer coneccion con {}'.format(imap_url))
        self.__set_connection_status(False)
        while not self.__connected:
            try:
                self.__connection = imaplib.IMAP4_SSL(imap_url)
            except Exception:
                # Reintentar si falla la conexion
                etype, evalue = sys.exc_info()[:2]
                estr = traceback.format_exception_only(etype, evalue)
                logstr = 'Fallo en conneccion con el servidor IMAP - '
                for each in estr:
                    logstr += '{0}; '.format(each.strip('\n'))
                logger1.error(logstr)
                time.sleep(5)
                continue 
            logger1.info('Coneccion establecida correctamente con el server')

            logger1.info('Iniciar Sesion: - {0}'.format(self.__user))

            try:
                login_res = self.__connection.login(self.__user, self.__password)
                logger1.info('Exitoso - {0}'.format(login_res))
            except Exception:
                # Halt script when login fails
                etype, evalue = sys.exc_info()[:2]
                estr = traceback.format_exception_only(etype, evalue)
                logstr = 'Fallido - '
                for each in estr:
                    logstr += '{0}; '.format(each.strip('\n'))
                logger1.critical(logstr)
                break
			
			
            logger1.info('Conectandose a la carpeta - {0}'.format(self.__source))
            try:
                result = self.__connection.select(self.__source)
                logger1.info('Carpeta seleccionada')
            except Exception:
                # Halt script when folder selection fails
                etype, evalue = sys.exc_info()[:2]
                estr = traceback.format_exception_only(etype, evalue)
                logstr = 'Fallo al seleccionar carpeta - '
                for each in estr:
                    logstr += '{0}; '.format(each.strip('\n'))
                logger1.critical(logstr)
                break

            logger1.info('Coneccion establecida correctamente')
            self.__set_connection_status(True)

    def connection_stablished(self) -> bool:
        return self.__connected
    
    def __set_connection_status(self, status:bool) -> bool:
        self.__connected = status
    
    def logout(self):
        try:
            self.__connection.logout()
        except Exception:
            logger1.error('Error en logout')
            pass
        self.__set_connection_status(False)

    def get_connection(self) -> imaplib.IMAP4_SSL:
        if self.__connection == '':
            logger1.error('Primero debe iniciar la coneccion con el metodo connect()')
        return self.__connection

    def search_email_matching_body_condition(self,word:str, unseen:str) -> EmailList:
        data=""
        conn = self.get_connection()
        if conn != "":
            try:
                search_result = self.__search(conn, 'BODY', word, unseen)
                data = self.__get_emails(conn, search_result)
            except:
                logger1.error('Error la obtener los emails, revisar conneccion con servidor')
        else:
            logger1.error('Debe inicializar primero la coneccion usando el metodo connect()')
        return  self.__transform_imap_messages(data)  

    def __search(self,connection: imaplib.IMAP4_SSL, key:str, value:str, unseen:str):
        data="";
        seen = '(UNSEEN)' if unseen == 'True' else '(SEEN)'
        logger1.info('Buscando emails criterio: {} , palabra clave: {} y estado: {}'.format(key, value,seen))
        try:
            result, data = connection.search(None, key, '"{}"'.format(value),seen)
        except imaplib.IMAP4.error:
            logger1.error('Error al realizar la busqueda de correos')
        return data
    
    def __transform_imap_messages(self, msgs:list) -> EmailList:
        messages_processed=list()
        for msg in msgs[::-1]:
            for sent in msg:
                if type(sent) is tuple:
                    dct=email.message_from_string(str(sent[1],'utf-8'))
                    email_subject = dct['subject']
                    email_from = dct['from']
                    dt_obj = parser.parse(dct['date'])
                    date=dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                    messages_processed.append(Email(e_from=email_from,subject=email_subject, date=date))
        return messages_processed

    def __get_emails(self,connection: imaplib.IMAP4_SSL,result_bytes:list) -> list:
        msgs = []
        try:
            emails = result_bytes[0].split()
            logger1.info('Emails encontrados: {}'.format(len(emails)))
            for num in emails:
                typ, data = connection.fetch(num, '(RFC822)')
                msgs.append(data)
            logger1.info('Emails procesados: {}'.format(len(msgs)))
        except imaplib.IMAP4.error:
            logger1.error('Error al obtener emails')
        return msgs