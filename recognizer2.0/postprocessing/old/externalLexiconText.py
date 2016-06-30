from externalLexicon import ExternalLexicon


class ExternalLexiconText(ExternalLexicon):
    def __init__(self):
        super(ExternalLexiconText, self).__init__()

    def execute(self, documents):
        lines = self._parse_documents(documents)
        words = self._parse_lines(lines)
        self._parse_words(words)

    def _parse_documents(self, documents):
        return super(ExternalLexiconText, self)._parse_documents(documents)

    def _parse_words(self, words):
        super(ExternalLexiconText, self)._parse_words(words)

    def _parse_lines(self, lines):
        """
        This will parse through all lines of the document and it will split them into words.
        :param lines: list(Str)
        :return:
        """
        words = []
        for line in lines:
            words += line.split(' ')
        return words

if __name__ == '__main__':
    E = ExternalLexiconText()
    E.execute(['lexicon1.txt', 'lexicon2.txt'])
