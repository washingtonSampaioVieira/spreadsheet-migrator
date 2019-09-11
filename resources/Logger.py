import logging
from dotenv import load_dotenv
import os
from config import Logs


class Logger:
    def __init__(self, filename):
        load_dotenv()

        # Configuração padrão para os Logs
        logging.basicConfig(
            level=os.getenv('LOGGER_LEVEL'),
            datefmt='%d/%m/%Y %H:%M:%S',
            format='%(levelname)s: %(message)s. Logged at %(asctime)s',
            handlers=[logging.FileHandler(Logs.LOG_FILE_PATH + filename, 'a+', 'utf-8')]
        )

    def info(self, message): logging.info(message)

    def error(self, message): logging.error(message)

    def warning(self, message): logging.warning(message)

    def debug(self, message): logging.debug(message)
