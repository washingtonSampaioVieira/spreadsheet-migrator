import pandas

class ExcelReader:
  def __init__(self, filename, options = None):
    default_options = { 'sheet_index': 0, 'skip_rows': 0, 'index_col': 0 }
    default_options.update(options)

    self.file = pandas.read_excel(filename, 
      sheet_name = default_options['sheet_index'], 
      skiprows = default_options['skip_rows'],
      index_col = default_options['index_col']
    )

  def read_file(self, format_function, limit = None):
    # Limitando o número de linhas lidas de acordo com parametro do usuário
    if limit != None and type(limit) == int: file = self.file[0:limit]
    else: file = self.file
    
    # Converte o arquivo para um objeto no formato (linha = [colunas])
    obj_dict = file.to_dict(orient='index')

    item_list = []

    for row in obj_dict.items():
      columns = row[1] # Colunas da linha atual
      id = row[0]

      item_list.append(format_function(id, columns))
    
    return item_list
