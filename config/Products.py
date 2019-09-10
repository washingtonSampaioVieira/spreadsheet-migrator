from . import DataType

def get_phone(data, treatment_function):
  return data['TELEFONE1']

PARABRISA_SOLICITATION_CONFIGURATION = {
  'filepath': 'C:\\Users\\gabriel.navevaiko\\Desktop\\GNV\\pára-brisa\\Solicitações\\SOLICITAÇÃO 1.xlsx',  
  'file_options': {
    'sheet_index': 1,
    'skip_rows': 0,
    'index_col': 0
  },
  'data_format': {
    'client': ('CNPJ', DataType.STR),
    'data': ('Data', DataType.DATA),
    'quantity': ('QTD', DataType.INT),
    'inicial_number': ('Nº Inicial', DataType.INT),
    'final_number': ('Nº Final', DataType.INT)
  }
}

PARABRISA_CLIENT_CONFIGURATION = {
  'filepath': 'C:\\Users\\gabriel.navevaiko\\Desktop\\GNV\\pára-brisa\\Banco de clientes\\C.CLIENTES.xls',  
  'file_options': {
    'sheet_index': 0,
    'skip_rows': 1,
    'index_col': 2
  },
  'data_format': {
    'cnpj': ('CNPJ', DataType.STR),
    'name': ('CLIENTE', DataType.STR),
    'address': ('ENDEREÇO', DataType.STR),
    'phone': (get_phone, DataType.PHONE),
  }
}