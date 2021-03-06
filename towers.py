#import pygame
import pygame.gfxdraw
from constants import tower_sprites, newSprite, sprite_towers, pygame

class Towers:
    damage = int
    tower_range = int
    fire_rate = int
    location = tuple
    target = None
    state = 0

    def __init__(self, location, damage=5, tower_range=50, fire_rate=1):
        self.damage = damage
        self.tower_range = tower_range
        self.fire_rate = fire_rate
        self.location = location
        self.sprite = newSprite(tower_sprites)
        self.sprite.move(location[0], location[1])
        self.create_hit_box(tower_range)
        sprite_towers.add(self.sprite)

    def update(self):
        self.sprite.changeImage(self.state)
        self.state = (self.state + 1) % 4

    def create_hit_box(self, tRange):
        self.tower_range = pygame.Surface(((tRange * 2) + 2, (tRange *2) + 2), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(self.tower_range, (tRange) + 1, (tRange) + 1, tRange, (0, 0, 0, 128))
        self.hit_box = Circle(self.tower_range)
        self.hit_box.rect.center = self.sprite.rect.center[0], self.sprite.rect.center[1]
        sprite_towers.add(self.hit_box)


    def __del__(self):
        sprite_towers.remove(self.sprite)

class Circle(pygame.sprite.Sprite):

    def __init__(self, srf):
        pygame.sprite.Sprite.__init__(self)
        self.image = srf
        self.rect = self.image.get_rect()

class Basic_tower(Towers):
    def __init__(self):
        pass

class Ice_tower(Towers):
    def __init__(self):
        pass
        