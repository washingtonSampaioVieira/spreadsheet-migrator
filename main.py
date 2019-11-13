# -*- coding: utf-8 -*-
# from resources.Watcher import EventHandler
# from watchdog.observers import Observer
# import time
# from config.Products import Teste
#
# path = 'C:\\Users\\gabriel.navevaiko\\Desktop\\'
# observer = Observer()
# observer.schedule(EventHandler(Teste()), path=path, recursive=False)


# print('Starting observer')
# observer.start()
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print('Stoping observer')
#     observer.stop()
#     observer.join()
# from modules.Solicitations import Solicitation
# from modules.Client import Client
# from config.Products import ParabrisaSolicitation, ParabrisaClient

# c = Client()
# s = Solicitation()

# print('Inserindo clientes')
# c.insert_clients(ParabrisaClient())
# print('Clients inserted')
# print('Inserindo solicitacoes')
# s.insert_solicitations(ParabrisaSolicitation())
# print('Solicitations inserted')


# ---------------------------------------
# este arquivo é o inivial para tudo
# Washington começa aqui !


from resources.ExcelReader import ExcelReader
from config import DatabaseField
from config.Products import ParabrisaSolicitation
from resources.File import File
from resources.DataFormat import DataFormat

# options = default_options = {'sheet_index': 1, 'skip_rows': 0, 'index_col': 0}


parabrisa = ParabrisaSolicitation()

planilha = ExcelReader(parabrisa.filepath, parabrisa.file_options)


format_parabrisa = DataFormat(parabrisa.data_format)

dados_formatados = planilha.read_file(format_parabrisa.format, 11)

file = File()
file.writeFile(dados_formatados, DatabaseField.PARA_BRISA)

# print(dados_formatados)
