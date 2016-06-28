import msgpack
import pickle


class ExternalLexicon(object):
    # TODO add save function
    # TODO add load function
    _word_lexicon = []
    _ch_lexicon = []

    def __init__(self):
        self._characters_to_be_discarderd = "-_+=(){}!?;.,\n"

    def _save(self, word_output_file, ch_output_file):
        word_output = open(word_output_file, 'w+b')
        ch_output = open(ch_output_file, 'w+b')

        pickle.dump(self._word_lexicon, word_output)
        pickle.dump(self._ch_lexicon, ch_output)

        word_output.close()
        ch_output.close()

    @staticmethod
    def _load(word_input_file, ch_input_file):
        word_input = open(word_input_file, 'rb')
        ch_input = open(ch_input_file, 'rb')

        word_model = pickle.load(word_input)
        ch_model = pickle.load(ch_input)

        word_input.close()
        ch_input.close()

        return {'word_model': word_model, 'ch_model': ch_model}

    @property
    def word_lexicon(self):
        return self._word_lexicon

    @property
    def character_lexicon(self):
        return self._ch_lexicon

    def _parse_documents(self, documents):
        """
        :param documents: list(Str)
        :return:
        """
        list_of_documents = []
        for document in documents:
            f = open(document, 'r')
            list_of_documents += f.readlines()
            f.close()

        return list_of_documents

    def _parse_words(self, words):
        """

        :param words: list(Str)
        :return:
        """
        for idx in range(len(words)):
            tmp_word = self._clean_term(words[idx])
            self._check_if_in_lexicon(words[idx], self._word_lexicon)
            self._parse_characters(list(tmp_word), self._ch_lexicon)

    def _parse_characters(self, characters, lexicon):
        """

        :param characters: list(Str)
        :param lexicon: list(Term)
        :return:
        """
        for idx, ch in enumerate(characters):
            self._check_if_in_lexicon(ch, lexicon)
        self._find_neighbours(characters)

    def _find_neighbours(self, characters, nbghrs=3):
        """

        :param characters: list(Str)
        :param nbghrs: Integer
        :return:
        """
        for idx, ch in enumerate(characters):
            for term in self._ch_lexicon:
                if term.term == ch:
                    for i in range(-nbghrs, 0):
                        if idx + i > 0:
                            tmp_ch = characters[idx + i]
                            term.left_neighbors(abs(i), tmp_ch)
                    for i in range(1, nbghrs + 1):
                        try:
                            tmp_ch = characters[idx + i]
                            term.right_neighbors(i, tmp_ch)
                        except IndexError:
                            continue

    def _check_if_in_lexicon(self, term, lexicon):  # , left_term=None, right_term=None
        """
        This will check if word exists in our lexicon and if not it will add it.
        :param term: Str
        :param lexicon: list(Term)
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
        :param term: Str
        :param lexicon: list(Term)
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
        :param term: Str
        :return:
        """
        term = str.lower(term)
        for ch in self._characters_to_be_discarderd:
            term = term.replace(ch, '')
        return term


class Term(object):
    def __init__(self, term, frequency=1):
        self.__term = term
        self.__frequency = frequency
        self._left_terms = {}
        self._right_terms = {}

    @property
    def term(self):
        return self.__term

    @property
    def frequency(self):
        return self.__frequency

    @property
    def left_neighbors(self):
        return self._left_terms

    def left_neighbors(self, distance, value):
        if value in self._left_terms[distance]:
            self._left_terms[distance][value] += 1
        else:
            self._left_terms[distance][value] = 1

    @property
    def right_neighbors(self):
        return self._right_terms

    def right_neighbors(self, distance, value):
        if value in self._right_terms[distance]:
            self._right_terms[distance][value] += 1
        else:
            self._right_terms[distance][value] = 1

    def increase_frequency(self):
        self.__frequency += 1

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class Character(Term):
    def __init__(self, character, neighbours=3):
        Term.__init__(self, character)
        for i in range(1, neighbours + 1):
            self._left_terms[i] = {}
            self._right_terms[i] = {}


class Word(Term):
    def __init__(self, word):
        Term.__init__(self, word)


if __name__ == '__main__':
    E = ExternalLexicon()
    E._parse_documents(['lexicon2.txt'])  # 'lexicon1.txt',
