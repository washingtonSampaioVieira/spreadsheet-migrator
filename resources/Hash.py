import hashlib
from config import DatabaseField


class MD5:

    def encrypter(self, dado):
        # generate hash de md5
        dadoUtf8 = dado.encode("utf8")
        hash_generated = hashlib.md5(dadoUtf8)

        return hash_generated.hexdigest()

    def encrypter_one(self, dado):

        text = self.format_strig(dado)
        text_hash = self.encrypter(text)
        dado_result = {DatabaseField.ID: dado[DatabaseField.ID], "hash": f"{text_hash}-{text}"}

        return dado_result

    def encrypter_all(self, dada):
        # encrypting all
        list_dada = []

        for record in dada:
            text = self.format_strig(record)
            text_hash = self.encrypter(text)
            list_dada.append({DatabaseField.ID: record[DatabaseField.ID], "hash": f"{text_hash}-{text}"})

        return list_dada

    def format_strig(self, dado):
        # formantando a string com um padrao de todos os dados em uma so linha
        string_format = "#"

        for key in dado.keys():
            if key == DatabaseField.OWNER_ID:
                return string_format

            string_format = f"{string_format}-{str(dado[key])}"

        return string_format
