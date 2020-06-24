import pygame
import os
from constants import loadImage, newSprite, sprite_terrain, window, grass_terrain, road_terrain, sprite_path

class Terrain(pygame.sprite.Sprite):
    level_Grass = (15, 150, 25)
    level_Road = (125, 25, 10)
    road = False
    can_place = True
    location = tuple
    colour = tuple
    grid_loc = tuple
    def __init__(self, path, pos, grid):
        self.road = path
        
        if path == True:
            self.sprite = newSprite(road_terrain, 8, 25)
            self.sprite.changeImage(1)
            self.sprite.move(pos[0], pos[1])
            self.colour = self.level_Road
            self.can_place = True
            sprite_path.add(self.sprite)
        else:
            self.sprite = newSprite(grass_terrain, 8, 25)
            self.sprite.changeImage(1)
            self.sprite.move(pos[0], pos[1])
            self.colour = self.level_Grass
            sprite_terrain.add(self.sprite) # adds tile to terrain sprite group
            
        self.location = pos
        self.set_ground()
        self.grid_loc = grid

    def set_ground(self):
        pass

    def __del__(self):
        pass