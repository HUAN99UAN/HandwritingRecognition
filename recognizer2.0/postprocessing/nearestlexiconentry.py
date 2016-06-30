import sys

import interface
import distancemeasures
from lexicon import Lexicon


class NearestLexiconEntry(interface.AbstractPostProcessor):

    def __init__(self, lexicon=None, distance_measure=distancemeasures.hamming_distance):
        super(NearestLexiconEntry, self).__init__()
        if not lexicon:
            self._lexicon = Lexicon.from_file()
        self._distance_measure = distance_measure

    def process(self, text):
        best_distance = sys.maxint
        best_match = None

        for entry in self._lexicon.entries():
            distance = self._distance_measure(entry.word, text)
            if distance < best_distance:
                best_match, best_distance = entry.word, distance
            if distance == 0:
                break
        return best_match

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
