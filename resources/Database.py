import os
from dotenv import load_dotenv
from deepdiff import DeepDiff
import mysql.connector as mysql

from . import Logger as LogModule
from config import DatabaseField

logger = LogModule.Logger('database.log')


class Database:
    @staticmethod
    def connect():
        connection = None

        load_dotenv()

        db_hostname = os.getenv('DB_HOSTNAME')
        db_user = os.getenv('DB_USERNAME')
        db_pass = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        try:
            connection = mysql.connect(host=db_hostname, user=db_user, passwd=db_pass, database=db_name)
        except mysql.errors.InterfaceError:
            logger.error('Error connecting to database, check .env file')

        return connection

    def insert_solicitation(self):
        # TODO: Check if owner is registered
        # TODO: Check if solicitation is already on database
        # TODO: Insert solicitation
        pass

    def owner_exists(self, cnpj):
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor(buffered=True)
        query = 'select proprietario_id from tbl_proprietario where cnpj = %s'

        try:
            cursor.execute(query, (cnpj,))

            row_count = cursor.rowcount

            db.close()
            return row_count != 0
        except mysql.errors.ProgrammingError as error:
            logger.error("Something went wrong on owner_exists function.\n\tDetails: %s" % error.msg)
            return False

    def insert_owner(self, client_data):
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor(dictionary=True)
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

            db.close()

            logger.info('Owner %s inserted' % client_data[DatabaseField.CNPJ])
            return result['@erro'] == 'Cadastrado'
        except mysql.errors.ProgrammingError and mysql.errors.IntegrityError as error:
            logger.error("Something went wrong on insert_client function.\n\tDetails: %s" % error.msg)
            return False

    def compare_owner_info(self, client_data, format_function):
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor(dictionary=True)
        query = 'select * from vw_info_proprietario where cnpj = %s'

        try:
            cursor.execute(query, (client_data[DatabaseField.CNPJ],))

            # TODO: Tratar caso em que o proprietário tem mais de um número de telefone ou email
            db_data = format_function(cursor.fetchone())

            # Removendo o ID do objeto
            client_data.pop('id')

            logger.debug('Client: %s\n\tDB data: %s\n\tReal data: %s' % (
                client_data[DatabaseField.CNPJ],
                db_data,
                client_data
            ))

            db.close()

            diff = DeepDiff(db_data, client_data)
            return diff
        except mysql.errors.ProgrammingError as error:
            logger.error("Something went wrong on compare_owner_info function.\n\tDetails: %s" % error.msg)
            return False

    def update_owner(self, cnpj, diffs):
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor(dictionary=True)

        obj_to_insert = {
            DatabaseField.CNPJ: cnpj,
            DatabaseField.NAME: '',
            DatabaseField.ADDRESS: '',
            DatabaseField.CEP: '',
            DatabaseField.CITY: '',
            DatabaseField.COMPANY_MANAGER: '',
            DatabaseField.PHONE: '',
            DatabaseField.EMAIL: '',
        }

        for diff in diffs:
            key = diff['key']
            value = diff['new_value']

            obj_to_insert[key] = value

        query = ('call atualizar_proprietario('
                 '%(' + DatabaseField.CNPJ + ')s, '
                 + '%(' + DatabaseField.NAME + ')s,'
                 + '%(' + DatabaseField.ADDRESS + ')s, '
                 + '%(' + DatabaseField.CEP + ')s, '
                 + '%(' + DatabaseField.CITY + ')s, '
                 + '%(' + DatabaseField.COMPANY_MANAGER + ')s,'
                 + '%(' + DatabaseField.PHONE + ')s, '
                 + '%(' + DatabaseField.EMAIL + ')s,'
                 + '@resultado)')

        try:
            cursor.execute(query, obj_to_insert)

            db.commit()

            query = 'select @resultado'
            cursor.execute(query)

            result = cursor.fetchone()

            db.close()

            logger.info('Owner %s updated' % cnpj)
            return result['@resultado'] >= 1
        except mysql.errors.ProgrammingError as error:
            print(cursor.statement)
            logger.error("Something went wrong on update_owner function.\n\tDetails: %s" % error.msg)
            return False
