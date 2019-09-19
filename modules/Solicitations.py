from resources.Database import Database
from resources.ExcelReader import ExcelReader
from resources.DataFormat import DataFormat
from resources.Logger import Logger
from config import DatabaseField


class Solicitation:
    def __init__(self):
        self.logger = Logger('solicitation_module.log')

    def insert_solicitations(self, product_config):
        db = Database()
        formatter = DataFormat(product_config.data_format)

        ex_reader = ExcelReader(product_config.filepath, product_config.file_options)
        solicitations = ex_reader.read_file(formatter.format, limit=1)

        total_solicitations = len(solicitations)
        inserted_solicitations_count = 0

        for solicitation in solicitations:
            sol_id = solicitation[DatabaseField.ID]
            solicitation_exists = db.solicitation_exists(sol_id, solicitation[DatabaseField.MODEL_ID])

            if solicitation_exists:
                self.logger.info('Solicitation %s already inserted' % sol_id)
                inserted_solicitations_count += 1
            else:
                sucess = db.insert_solicitation(solicitation)

                if sucess:
                    self.logger.info('Solicitation %s inserted with sucess' % sol_id)
                    inserted_solicitations_count += 1
                else:
                    self.logger.error('There was an erro on inserting solicitation %s' % sol_id)

        failed_solicitations_count = total_solicitations - inserted_solicitations_count

        self.logger.info('Inserted solicitations: \n\tSucess: %s\n\tFailure: %s' %
                         (inserted_solicitations_count, failed_solicitations_count))
