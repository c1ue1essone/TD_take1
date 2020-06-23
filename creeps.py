import pygame
from constants import draw, window, grid_size, menu_height, loadImage, newSprite, deer_sprite, sprite_creeps

class Creeps:
    health = int
    location = tuple
    grid_loc = 1
    speedx = .5
    speedy = .5
    creep_type = int
    creeps_blue = (25, 25, 210)
    creeps_red = (210, 75, 75)
    dirx = int
    diry = int
    def __init__(self, spawn):
        self.sprite = newSprite(deer_sprite[8])
        self.sprite.move(spawn[0],  spawn[1], True)
        sprite_creeps.add(self.sprite)
        self.location = pygame.Rect(spawn)
        self.health = 10
        self.dirx = 1
        self.diry = 0

    def update_location(self, route, grid_size):
        ### old pathfinding method based on hit boxs and fake barriers
        """self.location = pygame.Rect(self.location)
        hit_box = pygame.Rect(self.location).move(self.dirx * 4, self.diry * 4)
        if hit_box.left <= 0 or hit_box.right >= 600:
            self.dirx *= -1
        elif not hit_box.collidelist(boundary) == -1:
            self.change_dir()
        else:
            self.location = pygame.Rect(self.location).move(self.dirx, self.diry)"""
        self.find_loc(route)
        self.temp_location = self.speedx * self.dirx, self.speedy * self.diry
        self.location = pygame.Rect(self.location).move(self.dirx, self.diry)
        self.sprite.move(self.location[0],  self.location[1], True)

    def find_dirc(self, route):
        node = int(self.location.center[0] / grid_size), int((self.location.center[1] - menu_height) / grid_size)
        node_dist = route[0], route[1]

        if node[0] == node_dist[0]:
            self.dirx = 0
        elif node[0] > node_dist[0]:
            self.dirx = -1
        else:
            self.dirx = 1
        
        if node[1] == node_dist[1]:
            self.diry = 0
        elif node[1] > node_dist[1]:
            self.diry = -1
        else:
            self.diry = 1

    def find_loc(self, route):
        hit_box = pygame.Rect((route[self.grid_loc][0] * grid_size)+(grid_size/2), (route[self.grid_loc][1] * grid_size) + (menu_height + (grid_size/2)), 1, 1)
        if pygame.Rect(self.location.center[0], self.location.center[1], 1, 1).colliderect(hit_box):
            if self.grid_loc == len(route) - 1:
                return "end"
            else:
                self.grid_loc += 1
                self.find_dirc(route[self.grid_loc])
        """node = int(self.location.center[0] / 10), int((self.location.center[1] - 100) / 10)
        for i in range(len(route)):
            node_dist = route[i][0] - 1, route[i][1] - 1
            if node_dist == node:
                self.grid_loc = i + 1
                self.find_dirc(route[self.grid_loc])"""

    def __del__(self):
        pass