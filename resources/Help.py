from datetime import datetime
from resources.ExcelReader import ExcelReader
from config import DatabaseField
from config.Products import ParabrisaSolicitation
from config.Products import ParabrisaClient
from resources.File import File
from resources.DataFormat import DataFormat


def date_now():
    date_time = datetime.now()
    date_minutes_now = date_time.strftime("%d/%m/%Y %H:%M")
    return date_minutes_now


def init_parabrisa():
    date_current = date_now()

    print(f"backup start {DatabaseField.PARA_BRISA} at - {date_current}")

    # inicio o model
    windshield_spreadsheet = ParabrisaSolicitation()
    consumer_spreadsheet = ParabrisaClient()


    # instancia planilha
    spreadsheet_windshield = ExcelReader(windshield_spreadsheet.filepath, windshield_spreadsheet.file_options)
    spreadsheet_customer = ExcelReader(consumer_spreadsheet.filepath, consumer_spreadsheet.file_options)



    # formatar a data
    format_windshield = DataFormat(windshield_spreadsheet.data_format)
    format_consumer = DataFormat(consumer_spreadsheet.data_format)

    # le excel
    data_format_windshield = spreadsheet_windshield.read_file(format_windshield.format)
    data_format_customer = spreadsheet_customer.read_file(format_consumer.format)

    # compra os arquivos e faz o resto
    file = File()
    file.compare_file(data_format_windshield, DatabaseField.PARA_BRISA)
    file.compare_file(data_format_customer, DatabaseField.CONSUMER)
    return
