import sys

import interface
import distancemeasures
from lexicon import Lexicon


class NearestLexiconEntryWithPrior(interface.AbstractPostProcessor):

    def __init__(self, lexicon=None, distance_measure=distancemeasures.hamming_distance):
        super(NearestLexiconEntryWithPrior, self).__init__()
        if not lexicon:
            self._lexicon = Lexicon.from_file()
        self._distance_measure = distance_measure

    def process(self, text):
        best_score = sys.maxint
        best_match = None

        for entry in self._lexicon.entries():
            score = self._match_score(entry, text)
            if score < best_score:
                best_match, best_score = entry.word, score
            if score == 1:
                break
        return best_match

    def _match_score(self, entry, classified_word):
        distance = self._distance_measure(entry.word, classified_word)
        return entry.frequency * (1 - distance)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
