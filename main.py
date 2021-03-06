import sys
#import pygame
import random
import numpy
import pathfinder
from terrain import Terrain
from creeps import Pixie, Satyr, Dwarf, Deer, Druid, Hunter
from towers import Towers
from menus import Menus
from constants import pygame, grid_col, grid_row, grid_size, menu_height, screen_height, screen_width, screen, window, sprite_terrain, background, sprite_path, sprite_towers, time, sprite_creeps, wave_Count, clock, myfont, render_to_window

pygame.init()

class Game:
    path = [] # Path is render road
    minion = []
    towers = []
    road = [] # Used for A* process

    def __init__(self):
        self.run()
        self.spawn = tuple
        self.start = tuple
        self.end = tuple
    
    def load_level(self, progress):
        level_file = open("Level_" + str(progress))
        level = list(level_file.read().replace("\n", ""))[:(grid_col*(grid_row))]
        level_file.close()
        ground = []
        #ground = numpy.empty(shape = [grid_col, grid_row], dtype = object)

        #posx = grid_size / screen_width
        #posy = grid_size / screen_height
        for i, el in enumerate(level):
            posx = i%grid_col
            posy = (i//grid_col)
            if el == 'R':
                pos = (posx*grid_size, (posy*grid_size)+menu_height, (screen_width / grid_col), ((screen_height - menu_height) / grid_row))
                ground.append(Terrain(True, pos, (posx, posy)))
                self.road.append((posx, posy))
                self.path.append(Terrain(True, pos, (posx, posy)))
            elif el == 'S':
                pos = (posx*grid_size, (posy*grid_size)+menu_height, (screen_width / grid_col), ((screen_height - menu_height) / grid_row))
                ground.append(Terrain(True, pos, (posx, posy)))
                self.start = (posx, posy)
                self.road.append((posx, posy, (posx, posy)))
                self.spawn = ((posx*grid_size) - ((grid_size/2) - 2), ((posy*grid_size)+menu_height) + ((grid_size / 2) - 2), 4, 4)
                self.path.append(Terrain(True, pos, (posx, posy)))
            elif el == "F":
                pos = (posx*grid_size, (posy*grid_size)+menu_height, (screen_width / grid_col), ((screen_height - menu_height) / grid_row))
                ground.append(Terrain(True, pos, (posx, posy)))
                self.end = (posx, posy)
                self.road.append((posx, posy))
                self.path.append(Terrain(True, pos, (posx, posy)))
            else:
                pos = (posx*grid_size, (posy*grid_size)+menu_height, (screen_width / grid_col)-1, ((screen_height - menu_height) / grid_row)-1)
                ground.append(Terrain(False, pos, (posx, posy)))


        temp = numpy.array(ground)
        ground = temp.reshape(grid_col, grid_row)
        return ground

    def run(self):
        running = True
        tower_menu = Menus()
        frame = 1000
        tick = 16
        spawn_tick = 250
        
        #proof = Towers((5, 5))

        tower_menu.draw(screen)
        ground = self.load_level(2)

        sprite_terrain.draw(background) # Draws background terrain
        window.blit(background, (0, 0))

        pygame.display.update()

        grid = pathfinder.AStar()
        grid.init_path(grid_row, grid_col, self.road, self.start, self.end)
        route = grid.process()
        render_sprites = pygame.sprite.LayeredUpdates(sprite_terrain, sprite_path, layer=1)

        while running:

            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                ratio_x = (window.get_width() / screen.get_width())
                ratio_y = (window.get_height() / screen.get_height())
                mouse_scaled = (mouse_pos[0] / ratio_x, mouse_pos[1] / ratio_y)
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check for left button
                    if event.button == 1:
                    #    if tower_menu.basic_tower_button.collidepoint(mouse_scaled):
                    #         tower_menu.click(screen, tower_menu.basic_tower_button, True)
                    #     elif tower_menu.ice_tower_button.collidepoint(mouse_scaled):
                    #         tower_menu.click(screen, tower_menu.ice_tower_button, True)
                        for x in range(grid_col):
                            for y in range(grid_row):
                                if pygame.Rect(ground[x][y].location).collidepoint(mouse_scaled):
                                    if ground[x][y].can_place:
                                        self.towers.append(Towers(ground[x][y].location))
                                        ground[x][y].can_place = False
                                        render_sprites.add(sprite_towers, layer=2)
                        for num in range(len(self.minion)):
                            if self.minion[num].sprite.rect.collidepoint(mouse_scaled):
                                self.minion[num].health = 0
                # if event.type == pygame.MOUSEBUTTONUP:
                #     if event.button == 1:
                #         # if tower_menu.state:
                #         #     tower_menu.click(screen, tower_menu.basic_tower_button, False)
                # # if tower_menu.basic_tower_button.collidepoint(mouse_scaled) and not tower_menu.over:
                # #     tower_menu.hover(screen, tower_menu.basic_tower_button)
                # # elif tower_menu.over and not tower_menu.basic_tower_button.collidepoint(mouse_scaled):
                # #     tower_menu.hover_off(screen, tower_menu.basic_tower_button)

            if time() > tick:
                tick = time() + 17
                kill = []
                minion_hitboxs = []

                for num in range(len(self.minion)):
                    if self.minion[num]:
                        if not self.minion[num].alive:
                            kill.append(num)
                        elif self.minion[num].health > 0:
                            self.minion[num].update_location(route)
                            minion_hitboxs.append(self.minion[num].sprite.rect)

                if len(kill) > 0: # If there are minions to kill in the list this del them
                    for d in range(len(kill)):
                        del self.minion[kill[d]]
                    kill = []

                for num in range(len(self.towers)):
                    current_tower = self.towers[num]
                    collision_index = current_tower.hit_box.rect.collidelist(minion_hitboxs)
                    if not collision_index == -1 and current_tower.target == None:
                        current_tower.target = collision_index
                    elif not current_tower.target == collision_index:
                        current_tower.target = None
                    if not current_tower.target == None:
                        self.minion[current_tower.target].health -= current_tower.damage
                #Clears then render sprites to display
                render_sprites.remove_sprites_of_layer(3)
                render_sprites.add(sprite_creeps, layer=3)

            if time() > frame: # Update minion animation frames
                frame = 80 + time()
                for num in range(len(self.minion)):
                    if self.minion[num].health <= 0:
                        if self.minion[num].update(12) == "dead":
                            self.minion[num].alive = False
                    else:
                        self.minion[num].update()

                for num in range(len(self.towers)):
                    self.towers[num].update()

            if time() > spawn_tick:
                if wave_Count >= len(self.minion):
                    spawn_type = random.choice([Dwarf, Deer, Satyr, Hunter, Druid, Pixie])
                    #spawn_type = [Dwarf, Deer, Satyr, Hunter, Druid, Pixie]
                    self.minion.append(spawn_type(self.spawn))
                    spawn_tick = time() + 500
                render_sprites.add(sprite_creeps, layer = 3)

                #if wave_Count >= len(self.minion):
                #    self.minion.append(Deer(self.spawn))
                #    spawn_tick = time() + 500
                #render_sprites.add(sprite_creeps)

            clock.tick()
            render_sprites.draw(screen)
            #for num in range(len(self.towers)):
            #    screen.blit(self.towers[num].hit_box.image, (self.towers[num].sprite.rect.center))
            fps = myfont.render(str(int(clock.get_fps())), 1, (255, 255, 255), (15, 210, 50))
            screen.blit(fps, (20, screen_height - 30))
            window.blit((render_to_window(screen)), (0, 0))
            pygame.display.update()

if __name__ == "__main__":
    pygame.display.set_caption('Tower Defense')
    Game()
