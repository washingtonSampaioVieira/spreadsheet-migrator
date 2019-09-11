import os
from dotenv import load_dotenv
import mysql.connector as mysql
from . import Logger as LogModule
from config import DatabaseField

logger = LogModule.Logger('database.log')


class Database:
    def __init__(self):
        load_dotenv()

        db_hostname = os.getenv('DB_HOSTNAME')
        db_user = os.getenv('DB_USERNAME')
        db_pass = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        try:
            self.connection = mysql.connect(host=db_hostname, user=db_user, passwd=db_pass, database=db_name)
        except mysql.errors.InterfaceError:
            logger.error('Error connecting to database, check .env file')

    def insert_solicitation(self):
        # TODO: Check if owner is registered
        # TODO: Check if solicitation is already on database
        # TODO: Insert solicitation
        pass

    def owner_exists(self, cnpj):
        db = self.connection

        if db is None:
            return False

        cursor = db.cursor(buffered=True)
        query = 'select proprietario_id from tbl_proprietario where cnpj = %s'

        try:
            cursor.execute(query, (cnpj,))

            return cursor.rowcount != 0
        except mysql.errors.ProgrammingError as error:
            logger.error("Something went wrong on owner_exists function.\n\tDetails: %s" % error.msg)
            return False

    def insert_owner(self, client_data):
        db = self.connection

        if db is None:
            return False

        cursor = self.connection.cursor(dictionary=True)
        owner_exists = self.owner_exists(client_data[DatabaseField.CNPJ])

        if owner_exists:
            logger.debug("Owner %s exists, comparing info" % client_data[DatabaseField.CNPJ])
            client_is_up_to_date = self.compare_owner_info(client_data)

            if client_is_up_to_date:
                return True
            else:
                return False
        else:
            query = 'call cadastro_proprietario(%s, %s, %s, %s, %s, %s, %s, %s, "", %s, @erro)'

            try:
                cursor.execute(query, (
                    client_data[DatabaseField.NAME],
                    client_data[DatabaseField.CNPJ],
                    client_data[DatabaseField.CITY],
                    client_data[DatabaseField.UF],
                    client_data[DatabaseField.ADDRESS],
                    client_data[DatabaseField.CEP],
                    client_data[DatabaseField.COMPANY_MANAGER],
                    client_data[DatabaseField.PHONE],
                    client_data[DatabaseField.EMAIL]
                ))

                db.commit()

                query = 'select @erro'
                cursor.execute(query)

                result = cursor.fetchone()

                logger.info('Owner %s inserted' % client_data[DatabaseField.CNPJ])
                return result['@erro'] == 'Cadastrado'
            except mysql.errors.ProgrammingError and mysql.errors.IntegrityError as error:
                logger.error("Something went wrong on insert_client function.\n\tDetails: %s" % error.msg)
                return False

    def compare_owner_info(self, client_data):
        db = self.connection

        if db is None:
            return False

        cursor = db.cursor(dictionary=True)
        query = 'select * from vw_info_proprietario where cnpj = %s'

        try:
            cursor.execute(query, (client_data[DatabaseField.CNPJ],))

            db_data = cursor.fetchone()

            db_data.pop(DatabaseField.ID, None)
            client_data.pop(DatabaseField.ID, None)

            logger.debug('Client: %s\n\tDB data: %s\n\tReal data: %s' % (client_data[DatabaseField.CNPJ], db_data, client_data))

            # TODO: Compare info between both owners if is already registered
            # TODO: Format owners info before comparing
            if db_data == client_data:
                print('Clients are equal')
                return True
            else:
                # TODO: Update owner info
                print('Clients are different')
                return False
        except mysql.errors.ProgrammingError as error:
            logger.error("Something went wrong on compare_owner_info function.\n\tDetails: %s" % error.msg)
            return False

