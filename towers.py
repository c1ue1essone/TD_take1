import pygame
from constants import tower_sprites, newSprite, sprite_towers, window

class Towers:
    damage = int
    tower_range = int
    fire_rate = int
    location = tuple
    target = None
    state = 0
    #tower_type

    def __init__(self, location, damage = 5, tower_range = 5, fire_rate = 1):
        self.damage = damage
        self.tower_range = tower_range
        self.fire_rate = fire_rate
        self.location = location
        self.sprite = newSprite(tower_sprites, 4, 1)
        self.sprite.move(location[0], location[1])
        self.hit_box = pygame.draw.circle(window, (0, 0, 0), (self.sprite.rect.center[0], self.sprite.rect.center[1]), tower_range)
        sprite_towers.add(self.sprite)

    def update(self):
        self.sprite.changeImage(self.state)
        self.state = (self.state + 1) % 4

    def __del__(self):
        sprite_towers.remove(self.sprite)