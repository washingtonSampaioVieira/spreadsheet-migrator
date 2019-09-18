from resources.Database import Database
from resources.ExcelReader import ExcelReader
from resources.DataFormat import DataFormat
from config import Products, DatabaseField

db = Database()
product_config = Products.ParabrisaSolicitation()
formatter = DataFormat(product_config.data_format)

ex_reader = ExcelReader(product_config.filepath, product_config.file_options)
solicitations = ex_reader.read_file(formatter.format, limit=1)

for solicitation in solicitations:
    solicitation_exists = db.solicitation_exists(solicitation[DatabaseField.ID], solicitation[DatabaseField.MODEL_ID])

    if solicitation_exists:
        print('Solicitation %s already inserted' % solicitation[DatabaseField.ID])
    else:
        sucess = db.insert_solicitation(solicitation)

        if sucess:
            print('Solicitation %s inserted with sucess' % solicitation[DatabaseField.ID])
        else:
            print('There was an erro on inserting solicitation %s' % solicitation[DatabaseField.ID])