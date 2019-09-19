from resources.Database import Database
from resources.ExcelReader import ExcelReader
from resources.DataFormat import DataFormat
from resources.Logger import Logger
from config import DatabaseField


class Client:
    def __init__(self):
        self.logger = Logger('client_module.log')

    def insert_clients(self, product_config):
        db = Database()
        formatter = DataFormat(product_config.data_format)

        ex_reader = ExcelReader(product_config.filepath, product_config.file_options)
        clients = ex_reader.read_file(formatter.format, limit=3)

        inserted_clients_count = 0
        total_clients = len(clients)

        for client in clients:
            cnpj = client[DatabaseField.CNPJ]

            owner_exists = db.owner_exists(cnpj)

            if owner_exists:
                self.logger.info('Owner %s exists, comparing info' % cnpj)
                client_diff = db.compare_owner_info(client, formatter.format_db)

                if client_diff == {}:
                    self.logger.info('Client %s already inserted' % cnpj)
                    inserted_clients_count += 1
                else:
                    diffs = []

                    for item in client_diff['values_changed'].items():
                        key = item[0]
                        key = key[key.index('\'') + 1:key.index(']') - 1]
                        new_value = item[1]['new_value']

                        diffs.append({'key': key, 'new_value': new_value})

                    self.logger.debug('Updating client %s\n\tData:' % diffs)
                    sucess = db.update_owner(cnpj, diffs)

                    if sucess:
                        self.logger.info('Client %s updated' % cnpj)
                        inserted_clients_count += 1
                    else:
                        self.logger.error('Error updating client %s' % cnpj)
            else:
                sucess = db.insert_owner(client)

                if sucess:
                    self.logger.info('Client %s inserted' % cnpj)
                    inserted_clients_count += 1
                else:
                    self.logger.error('Error inserting client %s' % cnpj)

        failed_clients_count = total_clients - inserted_clients_count

        self.logger.info('Inserted clients: \n\tSucess: %s\n\tFailure: %s' %
                         (inserted_clients_count, failed_clients_count))
