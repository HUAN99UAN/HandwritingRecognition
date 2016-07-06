class Character:
    top = None
    left = None
    bottom = None
    right = None
    shear = None
    text = None

    @property
    def is_valid(self):
        return all([
            (self.right - self.left) > 5,
            (self.bottom - self.top) > 20,
            self.text != "^"
        ])

    def __repr__(self):
        return 'Character(top=%d, left=%d, bottom=%d, right=%d, shear=%d, text=%r)' % \
               (self.top, self.left, self.bottom, self.right, self.shear, self.text)


class Word:
    top = None
    left = None
    bottom = None
    right = None
    shear = None
    text = None

    def __init__(self):
        self.characters = []

    def __repr__(self):
        return 'Word(top=%d, left=%d, bottom=%d, right=%d, shear=%d, text=%r)' % \
               (self.top, self.left, self.bottom, self.right, self.shear, self.text)
