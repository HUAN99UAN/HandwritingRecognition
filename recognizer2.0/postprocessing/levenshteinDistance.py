import interface
import lexicon


class LevenshteinDistance(interface.AbstractPostProcessor):
    """
    https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    def __init__(self):
        pass
        #super(LevenshteinDistance, self).__init__()

    def _find_levenshtein_distance(self, word1, word1_len, word2, word2_len):
        """

        :param word1: word to be compared
        :param word1_len: the length of the first word
        :param word2: word to be compared
        :param word2_len: the length of thr second word
        :return: (int)
        """
        if word1_len == 0:
            return word2_len
        if word2_len == 0:
            return word1_len

        if word1[word1_len - 1] == word2[word2_len - 1]:
            cost = 0
        else:
            cost = 1

        return self._minimum(self._find_levenshtein_distance(word1, word1_len - 1, word2, word2_len) + 1,
                             self._find_levenshtein_distance(word1, word1_len, word2, word2_len - 1) + 1,
                             self._find_levenshtein_distance(word1, word1_len - 1, word2, word2_len - 1) + cost)

    def find_distance(self, lexicon_words, word):
        most_probable = {'lexicon_word': '', 'result_word': word, 'distance': 1000}
        dist = 100
        for lexicon_word in lexicon_words:
            new_dist = self._find_levenshtein_distance(word, len(word), lexicon_word.word, len(lexicon_word.word))
            if new_dist < dist:
                most_probable['lexicon_word'] = lexicon_word
                most_probable['distance'] = new_dist
                dist = new_dist

        print most_probable

    @staticmethod
    def _minimum(z, x, c):
        """
        :param z:
        :param x:
        :param c:
        :return: (int) return the minimum of the three params
        """
        if z < x:
            if x <= c:
                return z
            else:
                return c
        else:
            if c < x:
                return c
            else:
                return x


if __name__ == '__main__':
    l = LevenshteinDistance()
    lex = lexicon.Lexicon.from_file('lexicon.txt')
    l.find_distance(lex, 'qwerty')
