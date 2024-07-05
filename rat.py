import random
from constants import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE, WHITE
import pygame


# Rat class
class Rat:
    def __init__(self, color):
        self.position = (0, 0)
        self.color = color
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)
