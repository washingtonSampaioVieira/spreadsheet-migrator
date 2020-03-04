from config import DatabaseField
from resources import Logger
from resources.Hash import MD5
from deepdiff import DeepDiff
from resources.Database import Database
import re
import json
import os.path


def index_by_content(vector, item):
    for record in vector:
        record = json.loads(record)
        if record[DatabaseField.ID] == item[DatabaseField.ID]:
            return vector.index(record)


def update_request(product, item, item_old):
    with open(f'files/{product}.json', 'r') as file:
        lines = file.read()

        all_content = json.loads(lines)
        index = all_content.index(item_old)

    all_content[index] = item

    with open(f'files/{product}.json', 'w') as file:
        file.write(json.dumps(all_content))


def add_to_file(product, item):
    with open(f'files/{product}.json', 'r+') as file:
        lines = file.read()

        all_content = json.loads(lines)
        all_content.append(item)

    with open(f'files/{product}.json', 'w') as file:
        file.write(json.dumps(all_content))


def compare_objects(data1, data2):
    return DeepDiff(data1, data2)


def read_file_old(product):
    if os.path.exists(f"files/{product}.json") is not True:
        with open(f'files/{product}.json', 'x') as file:
            file.write("[]")

    with open(f'files/{product}.json', 'r') as old_file:
        print(product)
        str_file = old_file.read()
        json_file = json.loads(str_file)

    return json_file


class File:

    def __init__(self):
        self.logger = Logger.create_logger('Database', 'database.log')

    def compare_file(self, data, product):

        json_file_old = read_file_old(product)
        md5 = MD5()
        json_file_new = md5.encrypter_all(data)

        changes = compare_objects(json_file_old, json_file_new)
        changes_keys = changes.keys()

        if len(changes_keys) == 0:
            print("Neither a modification found.")
            return

        if "iterable_item_added" in changes_keys:
            print("added values")
            databases = Database()

            for key in changes['iterable_item_added']:
                index = int(re.sub('[^0-9]', '', key))

                result_insert = databases.insert(data[index])

                if result_insert:
                    md5 = MD5()
                    new_record = md5.encrypter_one(data[index])
                    add_to_file(product, new_record)

                    print(f"Save new request in file order {data[index][DatabaseField.ID]}  client {data[index][DatabaseField.CNPJ]} :) \n")
                    self.logger.info(f"Save new request in file order {data[index][DatabaseField.ID]}  client {data[index][DatabaseField.CNPJ]} :) \n")
                else:
                    md5 = MD5()
                    new_record = md5.encrypter_one(data[index])
                    add_to_file(product, new_record)
                    print(f"Not saved to log file order {data[index][DatabaseField.ID]} client {data[index][DatabaseField.CNPJ]} :( \n")
                    self.logger.info(f"Not saved to log file order {data[index][DatabaseField.ID]} client {data[index][DatabaseField.CNPJ]} :( \n")

        
        if "values_changed" in changes_keys:
            for key in changes['values_changed']:

                index = int(re.sub('[^0-9]', '', key))

                databases = Database()

                result_update = databases.update_status_solicitation(data[index])

                # correcting file information
                if result_update:
                    d5 = MD5()
                    new_record = md5.encrypter_one(data[index])

                    update_request(product, new_record, json_file_old[index])

                    print(f"old {data[index]} --- new {json_file_new[index]}")
                    print(f"Inserido no banco e no arquivo {data[index][DatabaseField.ID]}  client {data[index][DatabaseField.CNPJ]} \n")
                    self.logger.info(f"Inserido no banco e no arquivo {data[index][DatabaseField.ID]}  client {data[index][DatabaseField.CNPJ]} \n")

                else:
                    d5 = MD5()
                    new_record = md5.encrypter_one(data[index])

                    update_request(product, new_record, json_file_old[index])
                    print(f"Inserido no arquivo e nao inserido no banco {data[index][DatabaseField.ID]} client {data[index][DatabaseField.CNPJ]} \n")
                    self.logger.info(f"Inserido no arquivo e nao inserido no banco {data[index][DatabaseField.ID]} client {data[index][DatabaseField.CNPJ]} \n")
            return

