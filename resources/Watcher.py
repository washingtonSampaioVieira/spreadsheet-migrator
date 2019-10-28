from watchdog.events import FileSystemEventHandler
import json

from .ExcelReader import ExcelReader
from .DataFormat import DataFormat
from . import Logger


class EventHandler(FileSystemEventHandler):
    def __init__(self, file_config):
        self.logger = Logger.create_logger('EventHandler', 'eventhandler.log')
        self.file_config = file_config

    def on_modified(self, event):
        if self.file_config.filepath in event.src_path:
            ex_reader = ExcelReader(event.src_path)
            formatter = DataFormat(self.file_config.data_format)

            file = ex_reader.read_file(formatter.format, 5)

            # Lendo o arquivo backup
            with open('backups/usuarios.json', 'r') as json_file:
                try:
                    backup = json.load(json_file)
                except json.JSONDecodeError:
                    backup = {}

            # TODO: Comparar arquivo backup com arquivo atual

            if file == backup:
                print('Tudo OK')
            else:
                self.logger.debug('\n\tFile: %s\n\tBackup: %s' % (file, backup))
                print('Tudo errado')

            # Atualizando arquivo de backup
            with open('backups/usuarios.json', 'w') as json_file:
                json.dump(file, json_file)
