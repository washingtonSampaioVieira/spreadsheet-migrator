import os
from dotenv import load_dotenv
from deepdiff import DeepDiff
import mysql.connector as mysql
from config.Products import ParabrisaSolicitation
from config.DataType import INT

from . import Logger
from config import DatabaseField


class Database:
    def __init__(self):
        self.logger = Logger.create_logger('Database', 'database.log')

    def connect(self):
        connection = None

        load_dotenv()

        db_hostname = os.getenv('DB_HOSTNAME')
        db_user = os.getenv('DB_USERNAME')
        db_pass = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        try:
            connection = mysql.connect(host=db_hostname, user=db_user, passwd=db_pass, database=db_name)
        except mysql.errors.InterfaceError:
            self.logger.error('Error connecting to database, check .env file')

        return connection

    def solicitation_exists(self, solicitation_code, model_id):
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor(dictionary=True, buffered=True)
        query = 'select cod_autorizacao from tbl_autorizacao  where cod_autorizacao = %s and modelo_id = %s'

        try:
            cursor.execute(query, (solicitation_code, model_id))

            row_count = cursor.rowcount
            db.close()

            return row_count != 0
        except mysql.errors.ProgrammingError as error:
            self.logger.error("Something went wrong on solicitation_exists function.\n\tDetails: %s" % error.msg)
            return False

    def update_solicitation(self, solicitation):
        db = self.connect()
        if db is None:
            return False

        cursor = db.cursor()

        query = (
            'update tbl_autorizacao set numero_serie_inicial = %s, numero_serie_final = %s, qtde = %s, '
            'data_entrada = %s, modelo_id = %s where cod_autorizacao = %s and modelo_id = s%'
        )

        self.logger.info('Update solicitation %s' % solicitation)

        try:
            print(f"{solicitation[DatabaseField.INITIAL_NUMBER]}  numero inicial")
            print(f"{solicitation[DatabaseField.FINAL_NUMBER]}  numero final")
            print(f"{solicitation[DatabaseField.QUANTITY]}  quantidade")
            print(f"{solicitation[DatabaseField.ENTRY_DATE]}  data de entrada")
            print(f"{solicitation[DatabaseField.MODEL_ID]}  modelo id")
            print(f"{solicitation[DatabaseField.ID]}  solicitacao")
            print(f"{solicitation[DatabaseField.MODEL_ID]}  modelo id")

            cursor.execute(query, (
                solicitation[DatabaseField.INITIAL_NUMBER],
                solicitation[DatabaseField.FINAL_NUMBER],
                solicitation[DatabaseField.QUANTITY],
                solicitation[DatabaseField.ENTRY_DATE],
                solicitation[DatabaseField.MODEL_ID],
                solicitation[DatabaseField.ID],
                solicitation[DatabaseField.MODEL_ID]
            ))

            db.commit()

            row_count = cursor.rowcount
            db.close()
            return True

        except mysql.errors.ProgrammingError as error:
            self.logger.error("Something went wrong on update_solicitation function.\n\tDetails: %s" % error.msg)
            return False

    def insert_solicitation(self, solicitation):

        # solicitation already exists
        if self.solicitation_exists(solicitation[DatabaseField.ID], ParabrisaSolicitation.get_model_id(solicitation, INT)) is not False:
            print("Solicitação ja existente")
            return True

        db = self.connect()

        if db is None:
            return False

        solicitation[DatabaseField.OWNER_ID] = self.get_owner_id(solicitation[DatabaseField.CNPJ])

        cursor = db.cursor()
        query = (
            'insert into tbl_autorizacao(proprietario_id, cod_autorizacao, numero_serie_inicial, numero_serie_final, '
            'qtde, data_entrada, modelo_id) '
            'values(%s, %s, %s, %s, %s, %s, %s)'
        )

        self.logger.info('Inserting solicitation %s' % solicitation)
        print(solicitation)
        try:
            cursor.execute(query, (
                solicitation[DatabaseField.OWNER_ID],
                solicitation[DatabaseField.ID],
                solicitation[DatabaseField.INITIAL_NUMBER],
                solicitation[DatabaseField.FINAL_NUMBER],
                solicitation[DatabaseField.QUANTITY],
                solicitation[DatabaseField.ENTRY_DATE],
                solicitation[DatabaseField.MODEL_ID]
            ))

            db.commit()

            row_count = cursor.rowcount
            db.close()

            return row_count != 0
        except mysql.errors.ProgrammingError as error:
            print(error)
            self.logger.error("Something went wrong on insert_solicitation function.\n\tDetails: %s" % error.msg)
            return False

    def get_owner_id(self, cnpj):
        db = self.connect()

        owner_id = 0

        if db is None:
            return owner_id

        cursor = db.cursor(dictionary=True, buffered=True)
        query = 'select proprietario_id from tbl_proprietario where cnpj = %s limit 1'

        try:
            cursor.execute(query, (cnpj,))

            if cursor.rowcount == 0:
                return owner_id

            self.logger.info('Fetching owner id from cnpj: %s' % cnpj)

            owner = cursor.fetchone()
            owner_id = owner['proprietario_id']

            db.close()

            return owner_id
        except mysql.errors.ProgrammingError as error:
            self.logger.error("Something went wrong on get_owner_id function.\n\tDetails: %s" % error.msg)
            return owner_id

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
            self.logger.error("Something went wrong on owner_exists function.\n\tDetails: %s" % error.msg)
            return False

    def insert_owner(self, client_data):
        if self.owner_exists(client_data[DatabaseField.CNPJ]):
            print("Customer already registered")
            return True

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

            query = 'select @erro limit 1'
            cursor.execute(query)

            result = cursor.fetchone()

            db.close()

            self.logger.info('Owner %s inserted' % client_data[DatabaseField.CNPJ])
            print(client_data)
            return result['@erro'] == 'Cadastrado'
        except mysql.errors.ProgrammingError and mysql.errors.IntegrityError as error:
            self.logger.error("Something went wrong on insert_client function.\n\tDetails: %s" % error.msg)
            return False

    def compare_owner_info(self, client_data, format_function):
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor(dictionary=True)
        query = 'select * from vw_info_proprietario where cnpj = %s limit 1'

        try:
            cursor.execute(query, (client_data[DatabaseField.CNPJ],))

            db_data = format_function(cursor.fetchone())

            # Removendo o ID do objeto (Os ID's da planilha e do banco são diferentes)
            client_data.pop('id')

            self.logger.debug('Client: %s\n\tDB data: %s\n\tReal data: %s' % (
                client_data[DatabaseField.CNPJ],
                db_data,
                client_data
            ))

            db.close()

            diff = DeepDiff(db_data, client_data)
            return diff
        except mysql.errors.ProgrammingError as error:
            self.logger.error("Something went wrong on compare_owner_info function.\n\tDetails: %s" % error.msg)
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

        self.logger.info('Info to update on client %s:\n\t%s' % (cnpj, obj_to_insert))

        query = ('call atualizar_proprietario('
                 '%(' + DatabaseField.CNPJ + ')s, '
                                             '%(' + DatabaseField.NAME + ')s,'
                                                                         '%(' + DatabaseField.ADDRESS + ')s, '
                                                                                                        '%(' + DatabaseField.CEP + ')s, '
                                                                                                                                   '%(' + DatabaseField.CITY + ')s, '
                                                                                                                                                               '%(' + DatabaseField.COMPANY_MANAGER + ')s,'
                                                                                                                                                                                                      '%(' + DatabaseField.PHONE + ')s, '
                                                                                                                                                                                                                                   '%(' + DatabaseField.EMAIL + ')s,'
                                                                                                                                                                                                                                                                '@resultado)')

        try:
            cursor.execute(query, obj_to_insert)

            db.commit()

            query = 'select @resultado'
            cursor.execute(query)

            result = cursor.fetchone()

            db.close()

            self.logger.info('Owner %s updated' % cnpj)
            return result['@resultado'] >= 1
        except mysql.errors.ProgrammingError as error:
            self.logger.error("Something went wrong on update_owner function.\n\tDetails: %s" % error.msg)
            return False

    def insert(self, data):
        if DatabaseField.ENTRY_DATE in data.keys():
            self.insert_solicitation(data)

        elif DatabaseField.NAME in data.keys():
            self.insert_owner(data)

        return
