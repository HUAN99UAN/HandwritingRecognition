class CreateLexicon():

    @staticmethod
    def create(file_name):
        lexicon = []
        total_words = 0
        with open(file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1].split(' ')
                lexicon.append(LexiconWord(line[0], int(line[1])))
                total_words += int(line[1])

        for l in lexicon:
            l.frequency_in_text = (l.times_in_text*100.0)/total_words

        return lexicon


class LexiconWord():
    def __init__(self, word, times_in_text):
        self._word = word
        self._times_in_text = times_in_text
        self._frequency_in_text = 0

    @property
    def word(self):
        return self._word

    @property
    def times_in_text(self):
        return self._times_in_text

    @property
    def frequency_in_text(self):
        return self._frequency_in_text

    @frequency_in_text.setter
    def frequency_in_text(self, freq):
        self._frequency_in_text = freq

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

if __name__ == '__main__':
    c = CreateLexicon()
    print c.create('lexicon.txt')