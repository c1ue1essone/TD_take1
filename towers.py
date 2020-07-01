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

    def __init__(self, location, damage = 5, tower_range = 50, fire_rate = 1):
        self.damage = damage
        self.tower_range = tower_range
        self.fire_rate = fire_rate
        self.location = location
        self.sprite = newSprite(tower_sprites, 4, 1)
        self.sprite.move(location[0], location[1])
        self.hit_box_draw = pygame.Surface((tower_range * 2, tower_range * 2), pygame.SRCALPHA, 32)
        self.hit_box = pygame.draw.circle(self.hit_box_draw, (0, 0, 0), (tower_range, tower_range), tower_range, 1)
        #self.hit_box = pygame.draw.rect(self.hit_box_draw, (0, 0, 0), ((0, 0), (tower_range*2,tower_range*2)))
        sprite_towers.add(self.sprite)

    def update(self):
        self.sprite.changeImage(self.state)
        self.state = (self.state + 1) % 4

    def __del__(self):
        sprite_towers.remove(self.sprite)