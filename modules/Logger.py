import logging
import os
from config import config

class Logger:
  def __init__(self, filename):
    # Configuração padrão para os Logs
    logging.basicConfig(
      level = logging.DEBUG if os.environ.get('DEBUG') else logging.INFO,
      datefmt = '%d/%m/%Y %H:%M:%S',
      format = '%(levelname)s:%(message)s logged at %(asctime)s',
      filename = config.LOG_FILE_PATH + filename,
      filemode = 'a+'
    )
  
  def info(self, message): logging.info(message)
  def error(self, message): logging.error(message)
  def warning(self, message): logging.warning(message)
  def debug(self, message): logging.debug(message)
