import postprocessing as config


class Lexicon:

    def __init__(self, words):
        self._words = words

    @staticmethod
    def from_file(file_name=config.default_lexicon_file):
        lexicon = []
        total_words = 0
        with open(file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1].split(' ')
                lexicon.append(_Entry(line[0], int(line[1])))
                total_words += int(line[1])

        for l in lexicon:
            l.frequency = l.number_of_occurences / float(total_words)
        return Lexicon(words=lexicon)

    def entries(self):
        for entry in self._words:
            yield entry

    @property
    def longest_word(self):
        return max(self._words, key=lambda word: word.length)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class _Entry:
    def __init__(self, word, times_in_text):
        self._word = word
        self._occurences = times_in_text
        self._frequency = None

    @property
    def word(self):
        return self._word

    @property
    def number_of_occurences(self):
        return self._occurences

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency

    @property
    def length(self):
        return len(self._word)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
