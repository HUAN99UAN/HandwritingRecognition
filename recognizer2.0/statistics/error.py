class Error():
    """
    The name sucks we will change it later
    """

    def __init__(self):
        self._words_of_interest = ['Word', 'text=']
        self._length_of_text = 6
        self._total_words_compared = 0
        self._total_matched_words = 0
        self._mismatched_length = 0
        self._words = []

    def _compare(self, oracle, result):

        oracle_lines, result_lines = self._read_files(oracle=oracle, result=result)

        for line in range(len(oracle_lines)):
            if all(word in oracle_lines[line] for word in self._words_of_interest):
                print oracle_lines[line]
                oracle_word = self._extract_word(oracle_lines[line])
                result_word = self._extract_word(result_lines[line])
                self._compare_words(oracle_word, result_word)
                self._words.append(Word(oracle_word, result_word))

        return {'total_words': self._total_words_compared,
                'correct_words': self._total_matched_words,
                'wrong_words': self._total_words_compared - self._total_matched_words,
                'unequal_length': self._mismatched_length,
                'correctness_ratio': self._calculate_percentage()}

    def _calculate_percentage(self):
        return (self._total_matched_words * 100) / self._total_words_compared

    def _compare_words(self, oracle_word, result_word):
        self._total_words_compared += 1
        if len(oracle_word) != len(result_word):
            self._mismatched_length += 1
        elif oracle_word == result_word:
            self._total_matched_words += 1

    def _extract_word(self, line):
        start_pos = line.index(self._words_of_interest[1])
        end_pos = line.index('"', start_pos + self._length_of_text)
        return line[start_pos + self._length_of_text:end_pos]

    @staticmethod
    def _read_files(oracle, result):
        return open(oracle, 'r').readlines(), open(result, 'r').readlines()

    def _compare_multiple_files(self, oracle_files, result_files):
        results = {'total_words': [],
                   'correct_words': [],
                   'wrong_words': [],
                   'unequal_length': [],
                   'correctness_ratio': []}

        for oracle_file in range(len(oracle_files)):
            for result_file in range(len(result_files)):
                if oracle_file == result_file:
                    tmp_results = self._compare(oracle_file, result_file)
                    for k in results:
                        results[k].append(tmp_results[k])


class Word():
    def __init__(self, oracle_word, result_word):
        self._oracle_word = oracle_word
        self._result_word = result_word
        self._level_of_difference = 0
        self._unequal = False
        self._calculate_diff()

    @property
    def oracle_word(self):
        return self._oracle_word

    @property
    def result_word(self):
        return self._result_word

    @property
    def level_of_difference(self):
        return self._level_of_difference

    @property
    def are_of_eq_length(self):
        return self._unequal

    def _calculate_diff(self):
        if len(self._oracle_word) != len(self._result_word):
            self._unequal = True
            self._level_of_difference = abs(len(self._oracle_word) - len(self._result_word))
            return

        for idx in range(len(self._oracle_word)):
            if self._oracle_word[idx] == self._result_word[idx]:
                continue
            else:
                self._level_of_difference += 1

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


if __name__ == '__main__':
    e = Error()
    print e._compare('KNMP-VIII_F_69______2C2O_0004.words', 'KNMP-VIII_F_69______2C2O_0004(2).words') # KNMP-VIII_F_69______2C2O_0070.words
