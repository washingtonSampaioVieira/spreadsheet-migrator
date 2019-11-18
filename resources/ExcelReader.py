import pandas
from . import Logger


class ExcelReader:

    def __init__(self, file_path, options=None):
        self.logger = Logger.create_logger('ExcelReader', 'excelreader.log')

        default_options = {'sheet_index': 1, 'skip_rows': 10, 'index_col': 22}

        if options is not None:
            default_options.update(options)

        self.logger.info('Opening file %s with options %s' %
                         (file_path, options))
        self.file = pandas.read_excel(file_path,
                                      sheet_name=default_options['sheet_index'],
                                      skiprows=default_options['skip_rows'],
                                      index_col=default_options['index_col']
                                      )

    def read_file(self, format_function, limit=None):
        # Limitando o número de linhas lidas de acordo com parametro do usuário
        file = self.file.head(limit)
        # Converte o arquivo para um objeto no formato (linha = [colunas])
        obj_dict = file.to_dict(orient='index')

        item_list = []
        for row in obj_dict.items():
            columns = row[1]  # Colunas da linha atual

            if(type(columns) == float):
                print(columns)

            row_id = row[0]
            # Formata linha de acordo com função passada pelo usuário
            item_list.append(format_function(row_id, columns))
        return item_list
