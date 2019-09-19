import logging
from dotenv import load_dotenv
import os
from config import Logs


def create_logger(logger_name, file_name):
    load_dotenv()

    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(Logs.LOG_FILE_PATH + file_name, 'a+', 'utf-8')

    formatter = logging.Formatter('%(levelname)s: %(message)s. Logged at %(asctime)s')
    formatter.datefmt = '%d/%m/%Y %H:%M:%S'

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(logging.INFO if os.getenv('LOGGER_LEVEL') else logging.DEBUG)

    logger.info('Initiating logger %s on file %s' % (logger_name, file_name))

    return logger
