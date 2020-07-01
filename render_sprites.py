import pygame
from constants import sprite_towers, sprite_creeps, sprite_path, moving_sprites, window

class Render_sprites():
    def __init__(self):
        self.top_layer = pygame.sprite.LayeredUpdates(sprite_towers, sprite_creeps, sprite_path)
        self.top_layer.draw(window)

    def cDraw(self):
        self.top_layer.draw(window)