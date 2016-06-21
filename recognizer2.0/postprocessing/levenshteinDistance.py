import interface
import lexicon


class LevenshteinDistance(interface.AbstractPostProcessor):
    """
    https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    def __init__(self):
        super(LevenshteinDistance, self).__init__()

    def _find_levenshtein_distance(self, word1, word1_len, word2, word2_len):
        cost = 0
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
        most_probable = {'lexicon_word': '', 'result_word': word, 'distance': 100}
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
    l.find_distance(lex, 'asdf')
