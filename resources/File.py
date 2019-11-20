from resources.Hash import MD5
from deepdiff import DeepDiff
from resources.Database import Database
import re
import json




class File:
    def teste(self):
        print("A")

        # a = [{'id': 123, 'name': 'washington'},
        #      {'id': 124, 'name': 'lucas'},
        #      {'id': 125, 'name': 'jose'},
        #      {'id': 125, 'name': 'marcos'},
        #      {'id': 126, 'name': 'roberto'}]
        # b = [{'id': 123, 'name': 'washington'},
        #      {'id': 124, 'name': 'lucas'},
        #      {'id': 125, 'name': 'jose'},
        #      {'id': 125, 'name': 'marcos'},
        #      {'id': 126, 'name': 'roberto'},
        #      {'id': 127, 'name': 'washington'}]
        # res = ddiff = DeepDiff(a, b)
        #
        # if len(res) == 0:
        #     print("nada muda")
        #
        # if 'iterable_item_added' in res.keys():
        #     print("Existe mudanças")
        #
        # if 'values_changed' in res.keys():
        #     print("existe novos registros")

        # with open() as new_file:
        # new_file = open(f'files/{product}.json', 'a')
        # json_dados = json.dumps(list_of_hash)
        # print(json_dados)
        # new_file.write(json_dados)
        # print(file_old)
        # print(new_file.__dir__())
        # new_file.close()

        return "A"

    def compare_file(self, data, product):

        json_file_old = self.read_file_old(product)
        md5 = MD5()
        json_file_new = md5.encrypterAll(data)

        changes = self.compare_objects(json_file_old, json_file_new)
        changes_keys = changes.keys()

        if len(changes_keys) == 0:
            print("Neither a modification found.")
            return

        # ------

        if "iterable_item_added" in changes_keys:

            databases = Database()

            for key in changes['iterable_item_added']:

                index = int(re.sub('[^0-9]', '', key))
                print(data[index])
                result_insert = databases.insert_solicitation(data[index])

                # add new request to file of product
                if result_insert != 0:

                    md5 = MD5()
                    new_record = md5.encrypterOne(data[index])
                    self.add_to_file(product, new_record)

                    print("Save new request in file")

        # -------

        if "values_changed" in changes_keys:

            for key in changes['values_changed']:

                index = re.sub('[^0-9]', '', key)
                databases = Database()
                # result_insert = databases.update_solicitation(data[int(index)])
                result_insert = 1

                # correcting file information
                if result_insert != 0:

                    md5 = MD5()
                    new_record = md5.encrypterOne(data[int(index)])
                    self.update_request(product, new_record)

                    print("Update request to file")
        return

    def update_request(self, product, item):

        print("Updating to file...")

    def add_to_file(self, product, item):
        with open(f'files/{product}.json', 'r+') as file:
            lines = file.read()

            all_content = json.loads(lines)
            all_content.append(item[0])

        with open(f'files/{product}.json', 'w') as file:
            file.write(json.dumps(all_content))

    def compare_objects(self, data1, data2):
        return DeepDiff(data1, data2)

    def read_file_old(self, product):
        with open(f'files/{product}.json', 'r') as old_file:
            str_file = old_file.read()
            json_file = json.loads(str_file)

        return json_file
