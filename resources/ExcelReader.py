import pandas
from . import Logger as LogModule

logger = LogModule.Logger('logs.log')


class ExcelReader:
    def __init__(self, filename, options=None):
        default_options = {'sheet_index': 0, 'skip_rows': 0, 'index_col': 0}
        default_options.update(options)

        logger.info('Opening file %s with options %s' % (filename, options))

        self.file = pandas.read_excel(filename,
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
            row_id = row[0]

            # Formata linha de acordo com função passada pelo usuário
            item_list.append(format_function(row_id, columns))

        return item_list
