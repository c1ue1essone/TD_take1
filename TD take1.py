import pygame
import random
import sys

global spawn
#vars
screen_width, screen_height = 600, 600
grid_size = 60
grid_layout = [[0]*int((grid_size)) for _ in range(int((grid_size - 10)))]
creep_size = 4
path = []
creeps = []
creeps_Info = []
speedx = 5
speedy = 1
wave_Count = 10

pygame.init()
window = pygame.display.set_mode((screen_width, screen_height))
window.fill((0, 0, 0))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 25)

#Colours
menu_grey = (100, 100, 100)
creeps_Blue = (25, 25, 210)
creeps_Red = (210, 75, 75)
level_Grass = (15, 150, 25)
level_Road = (125, 25, 10)


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
    def __init__(self):
        pass

    def basic_tower(self):
        pass

class Creeps:
    def __init__(self):
        global creeps
        global creeps_Info
        #creeps.append(self)
        #creeps_health.append(self)

    def basic_creep(self, position):
        pass
        #position = pygame.Rect(position)
        #draw(window, creeps_Blue, position)
        #print(creeps)

    def hard_creep(self, position):
        draw(window, creeps_Red, position)

    def movement(self, posx, posy):
           pass
    
    def spawn_Creep(self):
        creeps.append(spawn)
        creeps_Info.append((random.randint(5, 10), random.randint(-5, 5)))

    def update_Move():
        for c in range(len(creeps)):
            #turn creeps pos data into Rects
            print(list(creeps[c]))
            t = list(creeps[c])
            i = list(creeps_Info[c])
            r = pygame.Rect(creeps[c])
            if not r.collidelist(path) == -1:
                t = list(creeps[c])
                t[0], t[1] = vector(t[0], t[1], i[0], i[1])
                creeps[c] = tuple(t)
                draw(window, creeps_Blue, creeps[c])

class Terran:
    def __init__(self):
        self.load_level(1)

    def load_level(self, progress):
        level_file = open("Level_" + str(progress))
        level = list(level_file.read().replace("\n", ""))[:(grid_size*(grid_size-10))]
        level_file.close()
        global path
        global spawn

        #posx = grid_size / screen_width
        #posy = grid_size / screen_height
        for i, el in enumerate(level):
            posx = i%grid_size
            posy = (i//grid_size)
            if el == 'R':
                self.position = ((posx*10, (posy*10)+100), ((screen_width / grid_size)-1, (screen_height / grid_size)-1))
                self.draw_road(window)
                path.append(pygame.Rect((posx*10, (posy*10)+100), (10, 10)))
            elif el == "S":
                self.position = ((posx*10, (posy*10)+100), ((screen_width / grid_size)-1, (screen_height / grid_size)-1))
                self.draw_road(window)
                spawn = (posx*10, (posy*10)+103, creep_size, creep_size)
                path.append(pygame.Rect((posx*10), (posy*10)+100, 10, 10))
            elif el == "F":
                self.position = ((posx*10, (posy*10)+100), ((screen_width / grid_size)-1, (screen_height / grid_size)-1))
                self.draw_road(window)
                path.append(pygame.Rect(posx*10, (posy*10)+100, 10, 10))
            else:
                self.position = ((posx*10, (posy*10)+100), ((screen_width / grid_size)-1, (screen_height / grid_size)-1))
                self.draw_grass(window)

            
    def ground(self):
        pass

    def draw_grass(self, surf):
        draw(surf, level_Grass, self.position)
    
    def draw_road(self, surf):
        draw(surf, level_Road, self.position)

class Game:
    def __init__(self):
        self.run()

    def run(self):
        running = True
        Menus()
        Terran()

        Menus().draw(window)
        Terran().load_level(1)
        pygame.display.update()
        
        for w in range(wave_Count):
            Creeps().spawn_Creep()

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
            
            # Update and clear path

            fps = myfont.render(str(int(clock.get_fps())), 1 , (255, 255, 255), level_Grass)
            window.blit(fps, (20, 570))

            
            for b in range(len(path)):
                draw(window, level_Road, path[b])
            
            Creeps.update_Move()

            pygame.display.update()
            clock.tick(60)
                    
#Level_1 = [[0]*int((screen_width/grid_size)) for _ in range(int((screen_height - 100)/grid_size))]
#progress = 1
#Level_file = open("Level_"+str(progress))
#Level = Level_file.readlines()
#print(Level)




if __name__ == "__main__":
    Game()
