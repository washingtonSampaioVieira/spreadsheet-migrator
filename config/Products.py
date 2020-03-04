from . import DataType
from . import DatabaseField


class ParabrisaSolicitation:
    filepath = '/home/ubuntu/wash.xlsm'

    @property
    def file_options(self):
        return {
            'sheet_index': 0,
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

    @property
    def get_name_plan(self):
        return DatabaseField.PARA_BRISA


class ParabrisaClient:
    filepath = '/home/ubuntu/Cadastro.de.Clientes.xlsx'

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

        for phone_key in ['TELEFONE1']:
            value = data[phone_key]
            if type(value) != float:
                formatted_phone_list.append(treatment_function(value))

        phones_str_list = ';'.join(formatted_phone_list)
        return value

    @property
    def get_name_plan(self):
        return DatabaseField.CONSUMER_PARA_BRISA


class CIPPClient:
    filepath = '/home/ubuntu/Cadastro.de.Clientes.xlsx'

    @property
    def file_options(self):
        return {
            'sheet_index': 0,
            'skip_rows': 1,
            'index_col': 0
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

        for phone_key in ['TELEFONE1']:
            value = data[phone_key]
            return value

    @property
    def get_name_plan(self):
        return DatabaseField.CONSUMER_CIPP


class CIPPSolicitation:
    filepath = '/run/user/1000/gvfs/smb-share:server=192.168.1.233,share=stor%201/Atendimento/Arquivos 17-18-19/BANCO DE DADOS/PRODUTOS PRIMI/SELOS DIVERSOS INMETRO/CIPP/Obsoleto/Solicitação cliente.xls'

    @property
    def file_options(self):
        return {
            'sheet_index': 0,
            'skip_rows': 0,
            'index_col': 0
        }

    @property
    def data_format(self):
        return {
            DatabaseField.ENTRY_DATE: ('DATA SOLICITAÇÃO', DataType.DATA),
            DatabaseField.INITIAL_NUMBER: ('Nº Inicial', DataType.INT),
            DatabaseField.FINAL_NUMBER: ('Nº Final', DataType.INT),
            DatabaseField.CNPJ: ('CNPJ', DataType.STR),
            DatabaseField.QUANTITY: ('QTD', DataType.INT),
            DatabaseField.MODEL_ID: (self.get_model_id, DataType.STR),
            DatabaseField.STATUS_SOLIC: ('STATUS.SOLIC', DataType.STR),
            DatabaseField.COD_RASTREIO: ('COD.RASTREIO', DataType.STR)


        }

    @staticmethod
    def get_model_id(data, treatment_function):
        return treatment_function(DatabaseField.CIPP_ID)

    @property
    def get_name_plan(self):
        return DatabaseField.CIPP_SOLICITATION
