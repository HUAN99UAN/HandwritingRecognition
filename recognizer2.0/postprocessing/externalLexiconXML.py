from externalLexicon import ExternalLexicon


class ExternalLexiconXML(ExternalLexicon):
    def __init__(self, word_flag):
        super(ExternalLexiconXML, self).__init__()
        self.__word_flag = word_flag
        self.__terms = ['word', 'form=']

    def execute(self, documents):
        lines = self._parse_documents(documents)
        words = self._parse_lines(lines)
        self._parse_words(words)

    def _parse_documents(self, documents):
        return super(ExternalLexiconXML, self)._parse_documents(documents)

    def _parse_words(self, words):
        super(ExternalLexiconXML, self)._parse_words(words)

    def _parse_lines(self, lines):
        """
        This will parse through all lines of the document and it will split them into words.
        :param lines: list(Str)
        :return:
        """
        words = []
        for line in lines:
            if all(string in line for string in self.__terms):
                words.append(line[line.find(self.__word_flag)+len(self.__word_flag):line.find('"',line.find(self.__word_flag)+len(self.__word_flag))])
        return words

if __name__ == '__main__':
    E = ExternalLexiconXML('form="')
    E.execute(['1999.02.0055.xml', '1999.02.0010.xml'])