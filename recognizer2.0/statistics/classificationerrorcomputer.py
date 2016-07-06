import inputOutput.wordio as wordio


def are_list_lengths_equal(a, b):
    if not (len(a) == len(b)):
        raise Exception("The lists should have the same number of elements.")


class ClassificationErrorComputer(object):

    def __init__(self, oracle=None, result=None, oracle_file=None, result_file=None):
        self._oracle = oracle if oracle else self._read_file(oracle_file)
        self._result = result if result else self._read_file(result_file)

        if not (bool(self._oracle) and bool(self._result)):
            raise TypeError("We need an oracle (file) and a result (file) to compute the error.")
        are_list_lengths_equal(self._oracle, self._result)
        self._number_correct_words, self._total_number_of_words = self._compute_error()

    @classmethod
    def _read_file(cls, words_file):
        if words_file:
            lines, _ = wordio.read(words_file)
            return lines

    def _compute_error(self):
        number_of_correctly_read_words = 0
        total_number_of_words = 0
        for line_pair in zip(self._oracle, self._result):
            total_number_of_words += len(line_pair[0])
            number_of_correctly_read_words += self._compute_line_error(*line_pair)
        return number_of_correctly_read_words, total_number_of_words

    def _compute_line_error(self, oracle, result):
        number_of_corectly_read_words = 0
        are_list_lengths_equal(oracle, result)
        for (oracle_word, result_word) in zip(oracle, result):
            number_of_corectly_read_words += int(oracle_word.text == result_word.text)
        return number_of_corectly_read_words

    @property
    def error(self):
        return 1 - self.recognition_rate

    @property
    def recognition_rate(self):
        return self._number_correct_words / float(self._total_number_of_words)


if __name__ == '__main__':
    oracle = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.words'
    actual = '/Users/laura/Desktop/output.words'
    e = ClassificationErrorComputer(oracle_file=oracle, result_file=actual)
    print e.error
