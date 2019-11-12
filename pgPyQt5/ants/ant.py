from custom_utils import Vector2D
from math import sin, cos, radians
from random import choice


class Ant:
    DIR_UP = Vector2D(0, 1)
    DIR_RIGHT = Vector2D(1, 0)
    DIR_DOWN = Vector2D(0, -1)
    DIR_LEFT = Vector2D(-1, 0)

    def __init__(self, ground, row, col, direction=DIR_UP):
        self.pos = Vector2D(row, col)
        self.ground = ground
        self.direction = direction
        self.ground.ants[self.pos.get()] = self

    @property
    def row(self):
        return self.pos.x

    @property
    def col(self):
        return self.pos.y

    def move(self):
        moves = self.get_possible_moves()
        move = choice(moves)
        del self.ground.ants[self.pos.get()]
        self.ground.ants[move.get()] = self
        self.direction = move - self.pos
        self.pos = move

    def rotate_direction(self, right=False):
        rads = radians(90)
        if right:
            rads *= -1
        new_x = cos(rads) * self.direction.x - sin(rads) * self.direction.y
        new_y = sin(rads) * self.direction.x + cos(rads) * self.direction.y

        return Vector2D(int(new_x), int(new_y))

    def get_possible_moves(self):
        possible_moves = []
        for d in [self.rotate_direction(right=False), self.direction, self.rotate_direction(right=True)]:
            move = self.pos + d
            if self.check_bounds(move):
                possible_moves.append(move)

        return possible_moves

    def check_bounds(self, pos):
        return 0 <= pos.x < self.ground.cols and 0 <= pos.y < self.ground.rows