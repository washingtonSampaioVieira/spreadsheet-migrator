from config import Products
from modules.Client import Client
from modules.Solicitations import Solicitation

client_module = Client()
client_module.insert_clients(Products.ParabrisaClient())

solicitation_module = Solicitation()
solicitation_module.insert_solicitations(Products.ParabrisaSolicitation())
