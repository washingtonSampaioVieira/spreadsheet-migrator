from . import DataType
from . import DatabaseField


class ParabrisaSolicitation:
    filepath = 'C:\\Users\\gabriel.navevaiko\\Desktop\\GNV\\pára-brisa\\Solicitações\\SOLICITAÇÃO 1.xlsx'

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
            DatabaseField.ENTRY_DATE: ('Data', DataType.DATA),
            DatabaseField.INITIAL_NUMBER: ('Nº Inicial', DataType.INT),
            DatabaseField.FINAL_NUMBER: ('Nº Final', DataType.INT),
            DatabaseField.CNPJ: ('CNPJ', DataType.STR),
            DatabaseField.QUANTITY: ('QTD', DataType.INT),
            DatabaseField.MODEL_ID: (self.get_model_id, DataType.INT)
        }

    @staticmethod
    def get_model_id(data, treatment_function):
        return treatment_function(5)


class ParabrisaClient:
    filepath = 'C:\\Users\\gabriel.navevaiko\\Desktop\\GNV\\pára-brisa\\Banco de clientes\\C.CLIENTES.xls'

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
            DatabaseField.NAME: ('CLIENTE', DataType.STR),
            DatabaseField.CNPJ: ('CNPJ', DataType.STR),
            DatabaseField.CITY: ('CIDADE', DataType.STR),
            DatabaseField.UF: ('UF', DataType.STR),
            DatabaseField.ADDRESS: ('ENDEREÇO', DataType.STR),
            DatabaseField.CEP: ('CEP', DataType.STR),
            DatabaseField.COMPANY_MANAGER: ('RESPONSAVEL', DataType.STR),
            DatabaseField.PHONE: (self.get_phone, DataType.PHONE),
            DatabaseField.EMAIL: ('E-MAIL', DataType.EMAIL)
        }

    def get_phone(self, data, treatment_function):
        formatted_phone_list = []

        for phone_key in ['TELEFONE1', 'TELEFONE2', 'TELEFONE3']:
            value = data[phone_key]
            if type(value) != float:
                formatted_phone_list.append(treatment_function(value))

        phones_str_list = ';'.join(formatted_phone_list)
        return phones_str_list
