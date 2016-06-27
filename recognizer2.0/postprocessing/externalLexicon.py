class ExternalLexicon(object):
    # TODO add save function
    # TODO add load function
    def __init__(self):
        self._word_lexicon = []
        self._ch_lexicon = []
        self._characters_to_be_discarderd = ";.,\n"

    def parse_documents(self, documents):
        """
        :param documents: list(Str)
        :return:
        """
        for document in documents:
            f = open(document, 'r')
            self._parse_lines(f.readlines())
            f.close()
        for c in self._ch_lexicon:
            print c
        print len(self._ch_lexicon)
        for w in self._word_lexicon:
            print w
        print len(self._word_lexicon)

    def _parse_lines(self, lines):
        """
        This will parse through all lines of the document and it will split them into words.
        :param lines: list(Str)
        :return:
        """
        for line in lines:
            self._parse_words(line.split(' '))

    def _parse_words(self, words):
        # TODO finish this
        for idx in range(len(words)):
            tmp_word = self._clean_term(words[idx])
            #self._check_if_in_lexicon(words[idx], self._word_lexicon)
            self._parse_characters(list(tmp_word), self._ch_lexicon)

    def _parse_characters(self, characters, lexicon):
        # TODO finish this
        for idx, ch in enumerate(characters):
            self._check_if_in_lexicon(ch, lexicon)
        self._find_neighbours(characters)
            # if (idx > 1) and (idx < len(characters) - 2):
            #     self._check_if_in_lexicon(ch, lexicon, characters[idx - 2], characters[idx + 2])
            # elif (idx > 0) and (idx < len(characters) - 1):
            #     self._check_if_in_lexicon(ch, lexicon, characters[idx - 1], characters[idx + 1])
            # else:

    def _find_neighbours(self, characters, nbghrs=3):
        for idx, ch in enumerate(characters):
            for term in self._ch_lexicon:
                if term.term == ch:
                    for i in range(-nbghrs, 0):
                        if idx+i > 0:
                            tmp_ch = characters[idx+i]
                            term.left_neighbors(tmp_ch)
                    for i in range(1, nbghrs+1):
                        try:
                            tmp_ch = characters[idx+i]
                            term.right_neighbors(tmp_ch)
                        except IndexError:
                            continue

    def _check_if_in_lexicon(self, term, lexicon):  # , left_term=None, right_term=None
        """
        This will check if word exists in our lexicon and if not it will add it.
        :param term:
        :param lexicon:
        :return:
        """
        for item in lexicon:
            if item.term == term:
                item.increase_frequency()
                return
        self._add_to_lexicon(term, lexicon)

    def _add_to_lexicon(self, term, lexicon):
        """
        This will create the new word object and add it to the lexicon
        :param term:
        :param lexicon:
        :return:
        """
        term = self._clean_term(term)
        if len(term) > 1:
            lexicon.append(Word(term))
        elif len(term) > 0:
            lexicon.append(Character(term))

    def _clean_term(self, term):
        """
        This will remove unwanted characters from the word.
        :param term:
        :return:
        """
        term = str.lower(term)
        for ch in self._characters_to_be_discarderd:
            term = term.replace(ch, '')
        return term

    def _check_neighbours(self, term):  # , left_term=None, right_term=None
        # TODO finish this
        for lex in self._word_lexicon:
            pass


class Term(object):
    def __init__(self, term, frequency=1):
        self.__term = term
        self.__frequency = frequency
        self.__left_terms = {}
        self.__right_terms = {}

    @property
    def term(self):
        return self.__term

    @property
    def frequency(self):
        return self.__frequency

    @property
    def left_neighbors(self):
        return self.__left_terms

    def left_neighbors(self, value):
        if value in self.__left_terms:
            self.__left_terms[value] += 1
        else:
            self.__left_terms[value] = 1

    @property
    def right_neighbors(self):
        return self.__right_terms

    def right_neighbors(self, value):
        if value in self.__right_terms:
            self.__right_terms[value] += 1
        else:
            self.__right_terms[value] = 1

    def increase_frequency(self):
        self.__frequency += 1

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class Character(Term):
    def __init__(self, character):
        Term.__init__(self, character)


class Word(Term):
    def __init__(self, word):
        Term.__init__(self, word)


if __name__ == '__main__':
    E = ExternalLexicon()
    E.parse_documents(['lexicon2.txt']) # 'lexicon1.txt',
