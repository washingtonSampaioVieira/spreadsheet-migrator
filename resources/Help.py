from datetime import datetime
from resources.ExcelReader import ExcelReader
from config import DatabaseField
from config.Products import ParabrisaSolicitation, CIPPClient, ParabrisaClient
from resources.File import File
from resources.DataFormat import DataFormat



def date_now():
    date_time = datetime.now()
    date_minutes_now = date_time.strftime("%d/%m/%Y %H:%M")
    return date_minutes_now


def get_data_format(obj):
    spreadsheet = ExcelReader(obj.filepath, obj.file_options)

    format_of_data = DataFormat(obj.data_format)
    data_format = spreadsheet.read_file(format_of_data.format)

    return data_format


def init_parabrisa():
    print(f"backup start {DatabaseField.PARA_BRISA} at - {date_now()}")

    windshields = [ParabrisaSolicitation(), CIPPClient()]

    file = File()

    for obj in windshields:
        data_format = get_data_format(obj)
        file.compare_file(data_format, obj.get_name_plan)

    return
