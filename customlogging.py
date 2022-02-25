import logging, sys
from logging.handlers import RotatingFileHandler

log = logging.getLogger('email_reader')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
handler_stdout = logging.StreamHandler(sys.stdout)
handler_stdout.setLevel(logging.DEBUG)
handler_stdout.setFormatter(formatter)
log.addHandler(handler_stdout)
handler_file = RotatingFileHandler(
	'email_reader.log',
	mode='a',
	maxBytes=1048576,
	backupCount=9,
	encoding='UTF-8',
	delay=True
	)
handler_file.setLevel(logging.DEBUG)
handler_file.setFormatter(formatter)
log.addHandler(handler_file)