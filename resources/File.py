from config import DatabaseField
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


class File:
    def compare_file(self, data, product):

        json_file_old = self.read_file_old(product)
        md5 = MD5()
        json_file_new = md5.encrypter_all(data)

        changes = self.compare_objects(json_file_old, json_file_new)
        changes_keys = changes.keys()

        if len(changes_keys) == 0:
            print("Neither a modification found.")
            return

        # ------



        if "iterable_item_added" in changes_keys:
            print("added values")
            databases = Database()

            for key in changes['iterable_item_added']:
                index = int(re.sub('[^0-9]', '', key))



                # chamar metodo de acordo com o produto
                databases.(product)('sss', 'aaa')




                result_insert = databases.insert_solicitation(data[index])
                # add new request to file of product
                if result_insert != 0:

                    md5 = MD5()
                    new_record = md5.encrypter_one(data[index])
                    self.add_to_file(product, new_record)

                    print("Save new request in file")

        # -------

        if "values_changed" in changes_keys:
            print("modified values")
            # for key in changes['values_changed']:
            #
            #     index = int(re.sub('[^0-9]', '', key))
            #
            #     databases = Database()
            #
            #     result_insert = databases.update_solicitation(data[index])
            #
            #     correcting file information
                # if result_insert != 0:
                #
                #     print(f"old {json_file_old[index]} --- new {json_file_new[index]}")
                #
                #     md5 = MD5()
                #     new_record = md5.encrypter_one(data[index])
                #     self.update_request(product, new_record, json_file_old[index])
                #
                #     print("Update request to file")
        # return

    def update_request(self, product, item, item_old):
        with open(f'files/{product}.json', 'r') as file:
            lines = file.read()

            all_content = json.loads(lines)
            index = all_content.index(item_old)

        all_content[index] = item

        with open(f'files/{product}.json', 'w') as file:
            file.write(json.dumps(all_content))


    def add_to_file(self, product, item):
        with open(f'files/{product}.json', 'r+') as file:
            lines = file.read()

            all_content = json.loads(lines)
            all_content.append(item)

        with open(f'files/{product}.json', 'w') as file:
            file.write(json.dumps(all_content))

    def compare_objects(self, data1, data2):
        return DeepDiff(data1, data2)

    def read_file_old(self, product):
        if os.path.exists(f"files/{product}.json") is not True:
            with open(f'files/{product}.json', 'x') as file:
                file.write("[]")

        with open(f'files/{product}.json', 'r') as old_file:
            print(product)
            str_file = old_file.read()
            json_file = json.loads(str_file)

        return json_file
