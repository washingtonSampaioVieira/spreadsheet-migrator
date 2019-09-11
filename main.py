from resources.Database import Database
from config import DatabaseField

db = Database()

c = {
    DatabaseField.NAME: 'CINETRAN C. DE INSP. E EQ. DE TRANSP. LTDA',
    DatabaseField.CNPJ: '05.632.361/0001-74',
    DatabaseField.CITY: 'DUQUE DE CAXIAS',
    DatabaseField.UF: 'RJ',
    DatabaseField.ADDRESS: 'ROD.WASHINGTON LUIZ 1951 - PARQUE DUQUE',
    DatabaseField.CEP: '25085-008',
    DatabaseField.COMPANY_MANAGER: 'CARLOS ROBERTO',
    DatabaseField.PHONE: '2136537800',
    DatabaseField.EMAIL: 'cinetran@cinetran.com.br',
    DatabaseField.LICENCE: ''
}


i = db.insert_owner(c)
print(i)
