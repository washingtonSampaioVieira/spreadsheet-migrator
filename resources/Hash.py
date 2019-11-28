import hashlib
from config import DatabaseField


class MD5:

    def encrypter(self, dado):
        # gerando hash de md5
        dadoUtf8 = dado.encode("utf8")
        hash = hashlib.md5(dadoUtf8)

        return hash.hexdigest()

    def encrypterOne(self, dado):
        dado_result = []
        text = self.formatStrig(dado)
        print(text)
        text_hash = self.encrypter(text)
        dado_result.append({DatabaseField.ID: dado[DatabaseField.ID], "hash": text_hash, "text_hash": text})
        return dado_result

    def encrypterAll(self, dados):
        # Criptografando todos
        list_dados = []
        for dado in dados:
            text = self.formatStrig(dado)
            text_hash = self.encrypter(text)
            list_dados.append({DatabaseField.ID: dado[DatabaseField.ID], "hash": text_hash, "text_hash": text})
        return list_dados

    def formatStrig(self, dado):
        # formantando a string com um padrao de todos os dados em uma so linha
        string_format = "#"
        for key in dado.keys():
            string_format = f"{string_format}-{str(dado[key])}"
        return string_format
