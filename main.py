from modules.DataFormat import DataFormat
from config.Products import PARABRISA_CLIENT_CONFIGURATION as config
from modules.ExcelReader import ExcelReader

formatter = DataFormat(config['data_format'])
ex_reader = ExcelReader(config['filepath'], config['file_options'])

my_list = ex_reader.read_file(formatter.format, 1)

for item in my_list:
  print(item)
