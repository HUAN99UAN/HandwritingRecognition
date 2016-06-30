import interface
import createLexicon


class HammingDistance(interface.AbstractPostProcessor):

    def __init__(self):
        pass
        #super(HammingDistance, self).__init__()

    def _find_hamming_distance(self, word1, word2):
        """
        https://en.wikipedia.org/wiki/Hamming_distance
        :param word1: word to be compared
        :param word2: word to be compared
        :return:
        """
        diff = 0
        if len(word1) != len(word2):
            cmp_data = self._return_shorter_and_diff(word1, word2)
            word1 = word1[:cmp_data['shortest']]
            word2 = word2[:cmp_data['shortest']]
            diff = cmp_data['difference']
        return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(word1, word2)) + diff

    @staticmethod
    def _return_shorter_and_diff(word1, word2):
        return {'shortest': max(len(word1), len(word2)), 'difference': abs(len(word1) - len(word2))}

    def find_distance(self, lexicon_words, word):
        most_probable = {'lexicon_word': '', 'result_word': word, 'distance': 100}
        dist = 100
        for lexicon_word in lexicon_words:
            new_dist = self._find_hamming_distance(lexicon_word.word, word)
            if new_dist < dist:
                most_probable['lexicon_word'] = lexicon_word
                most_probable['distance'] = new_dist
                dist = new_dist

        print most_probable

if __name__ == '__main__':
    h = HammingDistance()
    lex = createLexicon.CreateLexicon.create('lexicon.txt')
    h.find_distance(lex, 'qwerty')