from resources.Database import Database
from resources.ExcelReader import ExcelReader
from resources.DataFormat import DataFormat
from config import Products, DatabaseField

db = Database()
product_config = Products.ParabrisaClient()
formatter = DataFormat(product_config.data_format)

ex_reader = ExcelReader(product_config.filepath, product_config.file_options)
client = ex_reader.read_file(formatter.format, 1)[0]

owner_exists = db.owner_exists(client[DatabaseField.CNPJ])

if owner_exists:
    client_is_up_to_date = db.compare_owner_info(client, formatter.format_db)
    print(client_is_up_to_date)
    # if client_is_up_to_date:
    #     print('Client already inserted')
    # else:
    #     # TODO: Update client info
    #     pass
else:
    sucess = db.insert_owner(client)

    if sucess:
        print('Owner inserted with sucess')
    else:
        print('Error on inserting owner')
