

class ExternalLexicon():
    # TODO add save function
    # TODO add load function
    def __init__(self):
        self._lexicon = []

    def _parse_documents(self, documents):
        # TODO this is finished
        for document in documents:
            file = open(document, 'r')
            self._parse_lines(file.readlines())
            file.close()

    def _parse_lines(self, lines):
        # TODO this is finished
        for line in lines:
            self._parse_words(line.split(' '))

    def _parse_words(self, words):
        # TODO finish this
        for word in words:
            pass

    def _parse_characters(self, characters):
        # TODO finish this
        for character in characters:
            pass

    def _check_if_in_lexicon(self, word):
        # TODO finish this
        for lex in self._lexicon:
            if lex.word == word:
                lex.freq_increase()


    def _check_neighbours(self, word, left_word, right_word):
        # TODO finish this
        for lex in self._lexicon:
            pass


class Words():
    def __init__(self):
        # TODO add word
        # TODO add frequency
        # TODO add word to the right
        # TODO add word to the left
        pass

class Characters():
    def __init__(self):
        # TODO add character
        # TODO add frequency
        # TODO add char to the right
        # TODO add char to the left
        pass

