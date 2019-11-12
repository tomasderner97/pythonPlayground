from ant import Ant

class Ground:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.ants = {}
        self.food = {}
        self.paths = {}

        Ant(self, 100, 100)


