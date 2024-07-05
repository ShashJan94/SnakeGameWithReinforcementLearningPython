import random
import pygame
from constants import WHITE, GRID_SIZE, GRID_HEIGHT, GRID_WIDTH, UP, DOWN, LEFT, RIGHT


class Snake:
    def __init__(self, color, position=None):
        self.color = color
        self.positions = [position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow_to = 1
        self.alive = True

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if len(self.positions) > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x * GRID_SIZE, cur[1] + y * GRID_SIZE)

        # Check if the new position hits the wall
        if new[0] < 0 or new[0] >= GRID_WIDTH * GRID_SIZE or new[1] < 0 or new[1] >= GRID_HEIGHT * GRID_SIZE:
            self.alive = False
            return False

        # Check if the new position hits the snake itself
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.alive = False
            return False

        self.positions.insert(0, new)
        if len(self.positions) > self.grow_to:
            self.positions.pop()
        return True

    def grow(self):
        self.grow_to += 1

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    @staticmethod
    def randomize_position():

        return (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    @staticmethod
    def randomize_center_position():
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        offset = min(center_x, center_y) // 2

        position_x = random.randint(center_x - offset, center_x + offset) * GRID_SIZE
        position_y = random.randint(center_y - offset, center_y + offset) * GRID_SIZE

        return (position_x, position_y)
