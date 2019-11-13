import hashlib
from config import DatabaseField


class MD5:

    def encrypter(self, dado):
        # gerando hash de md5
        dadoUtf8 = dado.encode("utf8")
        hash = hashlib.md5(dadoUtf8)

        return hash.hexdigest()

    def encrypterAll(self, dados):
        # Criptografando todos
        listDados = []
        for dado in dados:
            text = self.formatStrig(dado)
            textHash = self.encrypter(text)
            listDados.append({DatabaseField.ID: dado[DatabaseField.ID], "hash": textHash})
        return listDados

    def formatStrig(self, dado):
        # formantando a string com um padrao de todos os dados em uma so linha
        stringFormat = "#"
        for key in dado.keys():
            stringFormat += "-" + str(dado[key])
        return stringFormat
