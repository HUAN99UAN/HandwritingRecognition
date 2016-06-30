import leven


def hamming_distance(word_1, word_2):
    length_difference = abs(len(word_1) - len(word_2))
    differences = [
        ord(character_1) != ord(character_2)
        for (character_1, character_2)
        in zip(word_1, word_2)
    ]
    return (sum(differences) + length_difference) / float(max(len(word_1), len(word_2)))


def edit_distance(word_1, word_2):
    distance = leven.levenshtein(word_1, str(word_2))
    return distance / float(max(len(word_1), len(word_2)))