#import pygame
from constants import screen_width, menu_height, draw, newSprite, tower_sprites, pygame, sprite_menu

class Menus:
    def __init__(self):
        self.menu = pygame.Rect((0, 0), (screen_width, menu_height))
        self.menu_grey = (100, 100, 100)
        self.current_button = object

    def draw(self, surf):
        draw(surf, self.menu_grey, self.menu)
        sprite_menu.draw(surf)
        #surf.blit(self.basic_tower_sprite.image, (32, 32))

class Menus_Button(pygame.sprite.Sprite):
    def __init__(self):
        self.menu_basic_tower()
        self.menu_ice_tower()
        self.menu_outline = (90, 90, 90)
        self.menu_hover = (110, 110, 110)
        self.over = False
        self.state = False

    def menu_basic_tower(self):
        self.basic_tower_button = pygame.Rect((20, 20), (40, 40))
        self.basic_tower_sprite = newSprite(tower_sprites, 4, 2)
        self.basic_tower_sprite.move(32, 32)
        sprite_menu.add(self.basic_tower_sprite)

    def menu_ice_tower(self):
        self.ice_tower_button = pygame.Rect((70, 20), (40, 40))
        self.ice_tower_sprite = newSprite(tower_sprites, 4, 2)
        self.ice_tower_sprite.changeImage(5)
        self.ice_tower_sprite.move(82, 32)
        sprite_menu.add(self.ice_tower_sprite)

    def draw(self, surf, button):
        draw(surf, self.menu_outline, button, 2)
        sprite_menu.draw(surf)
        #surf.blit(self.basic_tower_sprite.image, (32, 32))

    def create_icon(self, filename, index):
        pass

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

class Menu_Basic_Tower(Menus_Button):
    def __init__(self):
        super.__init__()
        # self.basic_tower_button = pygame.Rect((20, 20), (40, 40))
        # self.basic_tower_sprite = newSprite(tower_sprites, 4, 2)
        # self.basic_tower_sprite.move(32, 32)
        # sprite_menu.add(self.basic_tower_sprite)
        self.basic_tower_button = pygame.Rect((20, 20), (40, 40))
        self.basic_tower_sprite = newSprite(tower_sprites)
        
        

class Menu_Ice_Tower(Menus_Button):
    def __init__(self):
        self.ice_tower_button = pygame.Rect((70, 20), (40, 40))
        self.ice_tower_sprite = newSprite(tower_sprites, 4, 2)
        self.ice_tower_sprite.changeImage(5)
        self.ice_tower_sprite.move(82, 32)
        sprite_menu.add(self.ice_tower_sprite)
