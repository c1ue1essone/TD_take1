import pygame
from constants import screen_width, menu_height, draw

class Menus:
    def __init__(self):
        self.tower()
        self.menu = pygame.Rect((0,0), (screen_width, menu_height))
        self.menu_grey = (100, 100, 100)

    def tower(self):
        pass

    def draw(self, surf):
        draw(surf, self.menu_grey, self.menu)