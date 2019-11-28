from datetime import datetime
from resources.ExcelReader import ExcelReader
from config import DatabaseField
from config.Products import ParabrisaSolicitation
from resources.File import File
from resources.DataFormat import DataFormat


def date_now():
    date_time = datetime.now()
    date_minutes_now = date_time.strftime("%d/%m/%Y %H:%M")
    return date_minutes_now

def init_parabrisa():
    date_current = date_now()
    print(f"backup start {DatabaseField.PARA_BRISA} at - {date_current}")
    parabrisa = ParabrisaSolicitation()

    planilha = ExcelReader(parabrisa.filepath, parabrisa.file_options)

    format_parabrisa = DataFormat(parabrisa.data_format)
    data_format = planilha.read_file(format_parabrisa.format, 3)

    file = File()

    file.compare_file(data_format, DatabaseField.PARA_BRISA)
    return
