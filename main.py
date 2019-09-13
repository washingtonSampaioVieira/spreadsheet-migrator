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
    data_diff = db.compare_owner_info(client, formatter.format_db)

    if data_diff == {}:
        print('Client already inserted')
    else:
        diffs = []
        for item in data_diff['values_changed'].items():
            key = item[0]
            key = key[key.index('\'') + 1:key.index(']') - 1]
            new_value = item[1]

            diffs.append({'key': key, 'new_value': new_value})

        # TODO: Call db update_owner_info
else:
    success = db.insert_owner(client)

    if success:
        print('Owner inserted with sucess')
    else:
        print('Error on inserting owner')
