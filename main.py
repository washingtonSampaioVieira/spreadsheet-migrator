# from resources.Watcher import EventHandler
# from watchdog.observers import Observer
# import time
# from config.Products import Teste
#
# path = 'C:\\Users\\gabriel.navevaiko\\Desktop\\'
# observer = Observer()
# observer.schedule(EventHandler(Teste()), path=path, recursive=False)
#
# print('Starting observer')
# observer.start()
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print('Stoping observer')
#     observer.stop()
#     observer.join()
from modules.Solicitations import Solicitation
from modules.Client import Client
from config.Products import ParabrisaSolicitation, ParabrisaClient

c = Client()
s = Solicitation()

# print('Inserindo clientes')
# c.insert_clients(ParabrisaClient())
# print('Clients inserted')
print('Inserindo solicitações')
s.insert_solicitations(ParabrisaSolicitation())
print('Solicitations inserted')
