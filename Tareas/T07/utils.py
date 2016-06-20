from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


class BasicNL:
    words = stopwords.words('spanish')
    stemmer = SnowballStemmer('spanish', ignore_stopwords=True)

    @staticmethod
    def remove_stopwords(document):
        """
        Remueve las stopwords de del documento
        :param documento: lista de palabras de un documento
        :return: lista de palabras sin las stopwords
        """
        return list(filter(lambda x: x not in BasicNL.words, document))

    @staticmethod
    def apply_stemming(document):
        """
        Aplica stemming sobre el documento
        :param documento: lista de palabras de un documento sin stopwords
        :return: lista de palabras con stemming aplicado
        """
        return [BasicNL.stemmer.stem(x) for x in document]

# Deben haber descargado los corpus snowball_data y stopwords.
# Para esto deben ejecutar en consola
# import nktk
# nltk.download()
# En la interfaz seleccionar snowball_data y stopwords.

if __name__ == "__main__":
    doc = BasicNL.remove_stopwords(
        'estar aqui no yo el ellos hola numeros'.split(' '))
    print(BasicNL.apply_stemming(doc))
