import pygame
import random
import sys
import numpy
import pathfinder as A

global spawn
#vars
screen_width, screen_height = 600, 600
grid_size = 60
grid_layout = [[0]*int((grid_size)) for _ in range(int((grid_size - 10)))]
creep_size = 4
path = []
creeps = []
speedx = 5
speedy = 1
wave_Count = 10
boundary = []

pygame.init()
window = pygame.display.set_mode((screen_width, screen_height))
window.fill((0, 0, 0))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 25)

#Colours
menu_grey = (100, 100, 100)

def draw(surf, color, pos): 
    r = pygame.Rect(pos)
    pygame.draw.rect(surf, color, r)

def update_Path(surf):
    pass

def vector(travelx, travely, spx , spy):
    #milli = clock.tick()
    #print(milli)
    seconds = 1/120.
    dmx = seconds * spx
    dmy = seconds * spy
    x = dmx + travelx
    y = dmy + travely
    print("vector")
    return x, y

class Menus:
    def __init__(self):
        self.tower()
        self.menu = pygame.Rect((0,0), (screen_width, 100))

    def tower(self):
        pass

    def draw(self, surf):
        draw(surf, menu_grey, self.menu)

class Towers:
    damage = int
    tower_range = int
    fire_rate = int
    location = tuple
    #tower_type

    def __init__(self, location, damage = 5, tower_range = 5, fire_rate = 1):
        self.damage = damage
        self.tower_range = tower_range
        self.fire_rate = fire_rate
        self.location = location


    def create_tower(self):
        pass

class Creeps:
    health = int
    location = tuple
    grid_loc = 1
    route = int
    creep_type = int
    creeps_blue = (25, 25, 210)
    creeps_red = (210, 75, 75)
    dirx = int
    diry = int
    def __init__(self, spawn):
        self.location = pygame.Rect(spawn)
        self.health = 10
        draw(window, self.creeps_blue, self.location)
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
        
        self.find_dirc(route[self.grid_loc])
        self.location = pygame.Rect(self.location).move(self.dirx, self.diry)

    def find_dirc(self, route):
        node = int(self.location.center[0] / 10), int((self.location.center[1] - 100) / 10)
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
        """hit_box = pygame.Rect(route[self.grid_loc][0] * 10, (route[self.grid_loc][1] * 10) + 100, 1, 1)
        if pygame.Rect(self.location).colliderect(hit_box):
            self.grid_loc += 1"""
        node = int(self.location.center[0] / 10), int((self.location.center[1] - 100) / 10)
        for i in range(len(route)):
            node_dist = route[i][0] - 1, route[i][1] - 1
            if node_dist == node:
                self.grid_loc = i + 1
        self.find_dirc(self.route)

    def change_dir(self):
        hit_box = pygame.Rect(self.location)
        if self.dirx == 1 or self.dirx == -1:
            test_location = hit_box.move(0, -10)
            if test_location.collidelist(boundary) == -1:
                self.diry = -1
                self.dirx = 0
            else:
                self.diry = 1
                self.dirx = 0   
        elif self.diry == 1 or self.diry == -1:
            test_location = hit_box.move(10, 0)
            if test_location.collidelist(boundary) == -1:
                self.diry = 0
                self.dirx = 1
            else:
                self.diry = 0
                self.dirx = -1

    def __del__(self):
        pass

class Terrain:
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
            self.colour = self.level_Road
            self.can_place = True
        else:
            self.colour = self.level_Grass
        self.location = pos
        self.set_ground()
        self.grid_loc = grid

    def set_ground(self):
        pass

    def __del__(self):
        pass


class Game:
    path = []
    creep = []
    towers = []
    road = []
    col_count = 60
    row_count = 50

    def __init__(self):
        self.run()
    
    def load_level(self, progress):
        level_file = open("Level_" + str(progress))
        level = list(level_file.read().replace("\n", ""))[:(grid_size*(grid_size-10))]
        level_file.close()
        ground = []
        #ground = numpy.empty(shape = [self.col_count, self.row_count], dtype = object)
        global spawn
        global boundary

        #posx = grid_size / screen_width
        #posy = grid_size / screen_height
        for i, el in enumerate(level):
            posx = i%grid_size
            posy = (i//grid_size)
            if el == 'R':
                pos = (posx*10, (posy*10)+100, (screen_width / grid_size), (screen_height / grid_size))
                ground.append(Terrain(True, pos, (posx, posy)))
                self.road.append((posx, posy))
                self.path.append(Terrain(True, pos, (posx, posy)))
            elif el == "S":
                pos = (posx*10, (posy*10)+100, (screen_width / grid_size), (screen_height / grid_size))
                ground.append(Terrain(True, pos, (posx, posy)))
                self.start = (posx, posy)
                self.road.append((posx, posy, (posx, posy)))
                spawn = (posx*10, (posy*10)+103, creep_size, creep_size)
                self.path.append(Terrain(True, pos, (posx, posy)))
            elif el == "F":
                pos = (posx*10, (posy*10)+100, (screen_width / grid_size), (screen_height / grid_size))
                ground.append(Terrain(True, pos, (posx, posy)))
                self.end = (posx, posy)
                self.road.append((posx, posy))
                self.path.append(Terrain(True, pos, (posx, posy)))
            elif el =="B":
                boundary.append(pygame.Rect((posx*10, (posy*10)+100), ((screen_width / grid_size)-1, (screen_height / grid_size)-1)))
                pos = (posx*10, (posy*10)+100, (screen_width / grid_size)-1, (screen_height / grid_size)-1)
                ground.append(Terrain(False, pos, (posx, posy)))
            else:
                pos = (posx*10, (posy*10)+100, (screen_width / grid_size)-1, (screen_height / grid_size)-1)
                ground.append(Terrain(False, pos, (posx, posy)))


        temp = numpy.array(ground)
        ground = temp.reshape(self.col_count, self.row_count)
        return ground

    def run(self):
        running = True
        path = self.path
        Menus()

        Menus().draw(window)
        #Terran().load_level(1)
        ground = self.load_level(1)

        for x in range(self.col_count):
            for y in range(self.row_count):
                draw(window, ground[x][y].colour, ground[x][y].location)

        for i in range(len(path)):
            draw(window, path[i].colour, path[i].location)

        pygame.display.update()

        grid = A.AStar()
        grid.init_path(50, 60, self.road, self.start, self.end)
        route = grid.process()
        print(route)
        
        self.creep.append(Creeps(spawn))        

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
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

            for b in range(len(path)):
                draw(window, path[b].colour, path[b].location)

            self.creep[0].update_location(route, 10)
            draw(window, self.creep[0].creeps_blue, self.creep[0].location)
            pygame.display.update()
            clock.tick(60)
                    
#Level_1 = [[0]*int((screen_width/grid_size)) for _ in range(int((screen_height - 100)/grid_size))]
#progress = 1
#Level_file = open("Level_"+str(progress))
#Level = Level_file.readlines()
#print(Level)





if __name__ == "__main__":
    pygame.display.set_caption('Tower Defense')
    Game()
