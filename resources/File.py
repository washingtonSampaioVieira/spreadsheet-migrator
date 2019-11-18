from resources.Hash import MD5
from deepdiff import DeepDiff
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

    def compareArquivo(self, dados, product):

        json_file_old = self.readFileOld(product)
        md5 = MD5()
        json_file_new = md5.encrypterAll(dados)

        changes = DeepDiff(json_file_old, json_file_new)
        print(changes)
        changes_keys = changes.keys()

        if len(changes_keys) == 0:
            print("Nada muda")
            return

        if "iterable_item_added" in changes_keys:
            for key in changes['iterable_item_added']:
                indice  = re.sub('[^0-9]', '', key)
                print(f"Item modificado: {indice}")

                print(dados[int(indice)])


            print("Iten adicionado")

        if "values_changed" in changes_keys:
            print("Item modificado")

        return "B"

    def compareObjects(self, data1, data2):
        print("comprar arquivos")
        return False

    def readFileOld(self, product):
        with open(f'files/{product}.json', 'r') as old_file:
            str_file = old_file.read()
            json_file = json.loads(str_file)

        return json_file
