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

    def compare_owner_info(self, client_data, format):
        db = self.connection

        if db is None:
            return False

        cursor = db.cursor(dictionary=True)
        query = 'select * from vw_info_proprietario where cnpj = %s'

        try:
            cursor.execute(query, (client_data[DatabaseField.CNPJ],))

            db_data = format(cursor.fetchone())

            # logger.debug('Client: %s\n\tDB data: %s\n\tReal data: %s' % (client_data[DatabaseField.CNPJ], db_data, client_data))

            return True
        except mysql.errors.ProgrammingError as error:
            logger.error("Something went wrong on compare_owner_info function.\n\tDetails: %s" % error.msg)
            return False

