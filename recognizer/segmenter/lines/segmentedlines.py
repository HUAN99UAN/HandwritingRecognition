from segmenter.lines.psl import JoinedPieceWiseSeparatingLines


class SegmentedLines:
    def __init__(self):
        self._lines = list()

    def paint(self, image):
        for line in self._lines:
            line.paint(image)

    def add_line(self, line):
        self._lines.append(line)

    @staticmethod
    def from_psls(psls):
        lines = SegmentedLines()
        while psls:
            current_psl = psls[0]
            line = JoinedPieceWiseSeparatingLines.from_initial_psl(current_psl)
            lines.add_line(line)
            [psls.remove(psl) for psl in line.piece_wise_separating_lines]
        return lines