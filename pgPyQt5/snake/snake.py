import numpy as np
from numpy.random import randint
from numpy import array as arr
from custom_utils import Vector2D


class Snake:

    def __init__(self, width=50, height=50, direction="up", starvation_time=np.inf):

        self.width = width
        self.height = height
        self.direction = direction
        self.starvation_time = starvation_time
        self.body = [
            Vector2D(
                randint(0, width),
                randint(0, height)
            )
        ]
        self.food = None
        self.alive = True

        self.new_food()

    def new_food(self, x=-1, y=-1):

        if x < 0 or y < 0:
            while True:
                self.food = Vector2D(
                    randint(0, self.width),
                    randint(0, self.height)
                )

                if self.food not in self.body:
                    break
        else:
            if x >= self.width or y >= self.height:
                raise ValueError("Arguments out of bounds.")
            if Vector2D(x, y) in self.body:
                raise ValueError("There is a piece of body there.")

            self.food = Vector2D(x, y)

    def move(self):

        if self.direction == "up":
            new_x = self.head().x
            new_y = (self.head().y - 1) % self.height

        if self.direction == "right":
            new_x = (self.head().x + 1) % self.width
            new_y = self.head().y

        if self.direction == "down":
            new_x = self.head().x
            new_y = (self.head().y + 1) % self.width

        if self.direction == "left":
            new_x = (self.head().x - 1) % self.height
            new_y = self.head().y

        new_head = Vector2D(new_x, new_y)

        if new_head in self.body:
            self.alive = False

        self.body.insert(0, new_head)

        if new_head == self.food:
            self.new_food()
            return True
        else:
            self.body.pop()
            return False

    def head(self):

        return self.body[0]
