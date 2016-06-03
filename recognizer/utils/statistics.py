from collections import Counter


def mode(values):
    most_frequent_values = Counter(values)
    (most_frequent_value, _) = most_frequent_values.most_common(1)[0]
    return most_frequent_value