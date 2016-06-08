from sklearn.neighbors import KNeighborsClassifier


class Classifier:
    def __init__(self, model):
        self._classifier = KNeighborsClassifier(n_neighbors=1, p=2, n_jobs=-1)
        (patterns, labels) = model.patterns_and_labels
        self._classifier.fit(patterns, labels)

    def knn(self, character_image):
        feature_vector = character_image.feature_vector.reshape(1, -1)
        return self._classifier.predict(feature_vector)