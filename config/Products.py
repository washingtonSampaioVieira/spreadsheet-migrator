from . import DataType
from . import DatabaseField

class ParabrisaSolicitation:
    filepath = 'C:\\Users\\gabriel.navevaiko\\Desktop\\GNV\\pára-brisa\\Solicitações\\SOLICITAÇÃO 1.xlsx'

    properties = {
        'data': 'Data',
        'inicial_number': 'Nº Inicial',
        'final_number': 'Nº Final',
        'cnpj': 'CNPJ'
    }

    @property
    def file_options(self):
        return {
            'sheet_index': 1,
            'skip_rows': 0,
            'index_col': 0
        }

    @property
    def data_format(self):
        return {
            'data': (self.properties['cnpj'], DataType.DATA),
            'inicial_number': (self.properties['inicial_number'], DataType.INT),
            'final_number': (self.properties['final_number'], DataType.INT),
            'cnpj': (self.properties['cnpj'], DataType.STR),
            'quantity': (self.get_quantity, DataType.INT)
        }

    def get_quantity(self, data, treatment_function):
        inicial_number = data[self.properties['inicial_number']]
        final_number = data[self.properties['final_number']]

        return treatment_function(final_number - inicial_number + 1)


class ParabrisaClient:
    filepath = 'C:\\Users\\gabriel.navevaiko\\Desktop\\GNV\\pára-brisa\\Banco de clientes\\C.CLIENTES.xls'

    properties = {
        DatabaseField.CNPJ: 'CNPJ',
        DatabaseField.NAME: 'CLIENTE',
        DatabaseField.ADDRESS: 'ENDEREÇO',
        DatabaseField.CITY: 'CIDADE',
        DatabaseField.UF: 'UF',
        DatabaseField.CEP: 'CEP',
        DatabaseField.PHONE: ['TELEFONE1', 'TELEFONE2', 'TELEFONE3'],
        DatabaseField.COMPANY_MANAGER: 'RESPONSAVEL',
        DatabaseField.EMAIL: 'E-MAIL'
    }

    @property
    def file_options(self):
        return {
            'sheet_index': 0,
            'skip_rows': 1,
            'index_col': 2
        }

    @property
    def data_format(self):
        return {
            DatabaseField.NAME: (self.properties[DatabaseField.NAME], DataType.STR),
            DatabaseField.CNPJ: (self.properties[DatabaseField.CNPJ], DataType.STR),
            DatabaseField.CITY: (self.properties[DatabaseField.CITY], DataType.STR),
            DatabaseField.UF: (self.properties[DatabaseField.UF], DataType.STR),
            DatabaseField.ADDRESS: (self.properties[DatabaseField.ADDRESS], DataType.STR),
            DatabaseField.CEP: (self.properties[DatabaseField.CEP], DataType.STR),
            DatabaseField.COMPANY_MANAGER: (self.properties[DatabaseField.COMPANY_MANAGER], DataType.STR),
            DatabaseField.PHONE: (self.get_phone, DataType.PHONE),
            DatabaseField.EMAIL: (self.properties[DatabaseField.EMAIL], DataType.EMAIL)
        }

    def get_phone(self, data, treatment_function):
        formatted_phone_list = []

        for phone_key in self.properties[DatabaseField.PHONE]:
            value = data[phone_key]
            if type(value) != float:
                formatted_phone_list.append(treatment_function(value))

        phones_str_list = ';'.join(formatted_phone_list)
        return phones_str_list
