import pygame
from constants import screen_width, menu_height, draw, newSprite, tower_sprites, time

class Menus:
    def __init__(self):
        self.menu = pygame.Rect((0,0), (screen_width, menu_height))
        self.menu_basic_tower()
        self.menu_grey = (100, 100, 100)
        self.menu_outline = (90, 90, 90)
        self.menu_hover = (110, 110, 110)
        self.over = False

    def menu_basic_tower(self):
        self.basic_tower_button = pygame.Rect((20, 20), (40, 40))
        self.basic_tower_sprite = newSprite(tower_sprites, 4, 1)
        self.basic_tower_sprite.move(32, 32)

    def draw(self, surf):
        draw(surf, self.menu_grey, self.menu)
        draw(surf, self.menu_outline, self.basic_tower_button, 2)
        surf.blit(self.basic_tower_sprite.image, (32, 32))
    
    def hover(self, surf, button):
        draw(surf, self.menu_hover, button, 2)
        self.over = True
    
    def hover_off(self, surf, button):
        draw(surf, self.menu_outline, button, 2)
        self.over = False

    def click(self, surf, button, down):
        self.state = down
        if down:
            draw(surf, (130, 130, 130, 30), button)
            draw(surf, self.menu_hover, button, 2)
            surf.blit(self.basic_tower_sprite.image, (32, 32))
        else:
            self.draw(surf)
