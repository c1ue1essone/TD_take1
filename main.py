import sys
import pygame
import random
import numpy
import pathfinder
from terrain import Terrain
from creeps import Creeps
from towers import Towers
from menus import Menus
from constants import *

pygame.init()

class Game:
    path = [] # Path is render road
    minion = []
    towers = []
    road = [] # Used for A* process
    col_count = 60
    row_count = 50

    def __init__(self):
        self.run()
    
    def load_level(self, progress):
        level_file = open("Level_" + str(progress))
        level = list(level_file.read().replace("\n", ""))[:(grid_col*(grid_col-10))]
        level_file.close()
        ground = []
        #ground = numpy.empty(shape = [self.col_count, self.row_count], dtype = object)

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
        ground = temp.reshape(self.col_count, self.row_count)
        return ground

    def run(self):
        running = True
        path = self.path
        Menus()
        frame = 1000
        tick = 16

        Menus().draw(window)
        ground = self.load_level(1)

        for x in range(self.col_count):
            for y in range(self.row_count):
                pass
                #draw(window, ground[x][y].colour, ground[x][y].location)
        sprite_terrain.draw(window)

        for i in range(len(path)):
            draw(window, path[i].colour, path[i].location)

        pygame.display.update()

        grid = pathfinder.AStar()
        grid.init_path(grid_row, grid_col, self.road, self.start, self.end)
        route = grid.process()
        self.minion.append(Creeps(self.spawn))        

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check for left button
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for x in range(self.col_count):
                            for y in range(self.row_count):
                                if pygame.Rect(ground[x][y].location).collidepoint(mouse_pos):
                                    if ground[x][y].can_place == True:
                                        ground[x][y].colour = (0,0,255)
                                        draw(window, ground[x][y].colour, ground[x][y].location)
            
            # Update and clear path


            fps = myfont.render(str(int(clock.get_fps())), 1 , (255, 255, 255), (15, 210, 50))
            window.blit(fps, (20, 570))

            #Used for drawing just road without drawing whole screen

            #for b in range(len(path)):
            #    draw(window, level_Road, path[b])

            if time() > tick:
                tick = time() + 17
                for b in range(len(path)):
                    draw(window, path[b].colour, path[b].location)

                if self.minion[0].update_location(route, 10) == "end":
                    del self.minion[0]
                    #you died in the future
                else:
                    self.minion[0].update_location(route, 10)

            if time() > frame:
                frame = 80 + time()
                self.minion[0].update()

            sprite_creeps.draw(window)
            #draw(window, self.minion[0].creeps_blue, self.minion[0].location)
            pygame.display.update()

if __name__ == "__main__":
    pygame.display.set_caption('Tower Defense')
    Game()
