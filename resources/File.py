from resources.Hash import MD5


class File:
    def teste(self):
        print("A")
        return "A"

    def compareArquivo(self, dados, product):

        fileOld = self.readFileOld(product)

        md5 = MD5()
        list_of_hash = md5.encrypterAll(dados)

        new_file = open(f'files/{product}.json', 'a')
        new_file.write(str(list_of_hash))
        # print(new_file.__dir__())
        new_file.close()

        return "B"

    def compareObjects(self, data1, data2):
        print("comprar arquivos")
        return False

    def readFileOld(self, product):
        fileOld = open(f'files/{product}.json', r)
