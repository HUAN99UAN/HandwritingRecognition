import interface
from preprocessing import luminosity, morphological, otsu


class Pipe(interface.AbstractFilterBank):
    def __init__(self):
        self._filters = [
            luminosity.LuminosityNormalization(),
            morphological.Opening(),
            otsu.OtsuMethod()
        ]
