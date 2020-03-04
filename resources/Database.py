import os
from dotenv import load_dotenv
import mysql.connector as mysql


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
        query = 'select id_order from tb_order  where order_code = %s and id_product = %s limit 1'

        try:
            cursor.execute(query, (solicitation_code, model_id))
            result = cursor.fetchone()
            row_count = cursor.rowcount
            db.close()
            if result is not None:
                return result['id_order']
            else:
                return False
        except mysql.errors.ProgrammingError as error:
            self.logger.error("Something went wrong on solicitation_exists function.\n\tDetails: %s" % error.msg)
            return False

    def get_status_order(self, status):
        query = (f'select id_order_status from tb_order_status where status = "{status}" limit 1 ')
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor()
        try:
            cursor.execute(query)

            row_count = cursor.rowcount
            result = cursor.fetchone()
            id_order_status = result[0]

            return id_order_status
        except mysql.errors.ProgrammingError as error:
            print(error)
            self.logger.error("Something went wrong on select tb_order_status function.\n\tDetails: %s" % error.msg)
            return False

    def update_finished_status(self, id_order):
        db = self.connect()
        if db is None:
            return False

        query = (
            f'UPDATE `tb_rel_order_status` SET `finished_at` = NOW() WHERE `id_order` = "{id_order}" and '
            '`finished_at` is null'
        )
        cursor = db.cursor()
        try:
            cursor.execute(query)

            db.commit()
            row_count = cursor.rowcount
            db.close()
            return row_count != 0
        except mysql.errors.ProgrammingError as error:
            self.logger.error("Something went wrong on update_ function.\n\tDetails: %s" % error.msg)
            return False
        return True

    def update_status_solicitation(self, solicitation):
        db = self.connect()
        if db is None:
            return False
        id_system_user = self.get_user_from_client_cnpj(solicitation[DatabaseField.CNPJ])

        id_status_order = self.get_status_order(solicitation[DatabaseField.STATUS_SOLIC])

        id_order = self.solicitation_exists(solicitation[DatabaseField.ID], DatabaseField.CIPP_ID)

        if id_system_user and id_status_order and id_order:
            self.update_finished_status(id_order)
        else:
            print("unregistered client")
            self.logger.info("Unregistered client")
            return False

        query = (
            'INSERT INTO `tb_rel_order_status`'
            '(`id_order_status`, `id_status_order`, `id_system_user`, `id_order`, `created_at`, `updated_at`, '
            '`finished_at`) '
            f'VALUES (UUID(), "{id_status_order}", "{DatabaseField.ID_SYSTEM_USER}", "{id_order}", NOW(), NOW(), NULL)'
        )

        self.logger.info('Create new status solicitaion%s' % solicitation)
        cursor = db.cursor()
        try:
            cursor.execute(query)

            db.commit()

            row_count = cursor.rowcount
            db.close()
            return row_count != 0

        except mysql.errors.ProgrammingError as error:
            print(error)
            self.logger.error("Something went wrong on update_status_solicitation function.\n\tDetails: %s" % error.msg)
            return False

    def get_user_from_client_id(self, id_client):
        query = ('select id_client_user from tb_client_print_log as cl '
                 f'inner join tb_client_user as u on u.id_client = cl.id_client  where cl.id_client_print_log = "{id_client}" limit 1 ')
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor()
        try:
            cursor.execute(query)

            row_count = cursor.rowcount
            result = cursor.fetchone()
            id_client_user = result[0]

            return id_client_user
        except mysql.errors.ProgrammingError as error:
            print(error)
            self.logger.error("Something went wrong on get_user_from_client_id function.\n\tDetails: %s" % error.msg)
            return False

    def get_user_from_client_cnpj(self, cnpj):
        query = ('select id_client_user from tb_client_print_log as cl '
                 f'inner join tb_client_user as u on u.id_client = cl.id_client  where cl.cnpj = "{cnpj}" limit 1 ')
        db = self.connect()

        if db is None:
            return False

        cursor = db.cursor()
        try:
            cursor.execute(query)

            result = cursor.fetchone()
            if result != None:
                id_client_user = result[0]
                return id_client_user
            else:
                return False


        except mysql.errors.ProgrammingError as error:
            print(error)
            self.logger.error("Something went wrong on get_user_from_client_cnpj function.\n\tDetails: %s" % error.msg)
            return False

    def insert_solicitation(self, solicitation):

        # solicitation already exists
        if self.solicitation_exists(solicitation[DatabaseField.ID], DatabaseField.CIPP_ID) is not False:
            print("Solicitação ja existente")
            return True

        db = self.connect()

        if db is None:
            return False

        solicitation[DatabaseField.OWNER_ID] = self.get_owner_id(solicitation[DatabaseField.CNPJ])

        if solicitation[DatabaseField.OWNER_ID] == 0:
            print(solicitation[DatabaseField.CNPJ])
            print("Nem um propritario cadastrado com o CNPJ desta solicitação")
            return False
        solicitation[DatabaseField.CLIENT_USER] = self.get_user_from_client_id(solicitation[DatabaseField.OWNER_ID])

        if solicitation[DatabaseField.CLIENT_USER] == 0:
            print("Empresa não tem usuário cadastrado")
            return False

        cursor = db.cursor()
        query = (
            'INSERT INTO `tb_order`(`id_order`, `id_client_user`, `id_product`, `id_delivery_type`, `id_log_client`, '
            '`order_code`, `quantity`, `initial_number`, `final_number`, `created_at`, `updated_at`) '
            'VALUES  (UUID(), %s, %s,  %s, %s, %s, %s, %s, %s, NOW(), NOW())'
        )

        self.logger.info('Inserting solicitation %s' % solicitation)
        try:
            cursor.execute(query, (
                solicitation[DatabaseField.CLIENT_USER],
                DatabaseField.CIPP_ID,
                DatabaseField.DELIVERY_TYPE_WITHDRAWAL,
                solicitation[DatabaseField.OWNER_ID],
                solicitation[DatabaseField.ID],
                solicitation[DatabaseField.QUANTITY],
                solicitation[DatabaseField.INITIAL_NUMBER],
                solicitation[DatabaseField.FINAL_NUMBER],
            ))
            db.commit()

            row_count = cursor.rowcount
            db.close()

            return row_count != 0
        except mysql.errors.ProgrammingError as error:
            print(error)
            self.logger.error("Something went wrong on insert_solicitation function.\ntDetails: %s" % error.msg)
            return False

    def get_owner_id(self, cnpj):
        db = self.connect()

        owner_id = 0

        if db is None:
            return owner_id

        cursor = db.cursor(dictionary=True, buffered=True)
        query = 'select id_client_print_log from tb_client_print_log where cnpj = %s limit 1'

        try:
            cursor.execute(query, (cnpj,))

            if cursor.rowcount == 0:
                return owner_id

            self.logger.info('Fetching owner id from cnpj: %s' % cnpj)

            owner = cursor.fetchone()
            owner_id = owner['id_client_print_log']

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

    def insert(self, data):
        if DatabaseField.ENTRY_DATE in data.keys():
            return self.insert_solicitation(data)

        # elif DatabaseField.NAME in data.keys():
        #     return self.insert_owner(data)
