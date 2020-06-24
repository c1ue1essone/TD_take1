import os
import pygame

pygame.font.init()

creep_size = 4
path = []
wave_Count = 10
menu_height = 100
grid_size = 16
grid_col = 60
grid_row = 50
grid_layout = [[0]*int(grid_col) for _ in range(int(grid_row))]
screen_width, screen_height = grid_col * grid_size, (grid_row * grid_size) + menu_height
window = pygame.display.set_mode((screen_width, screen_height))
window.fill((0, 0, 0))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 25)
game_dir = os.path.dirname(__file__)
game_assets = os.path.join(game_dir, "assets")
sprite_terrain = pygame.sprite.OrderedUpdates()
sprite_creeps = pygame.sprite.OrderedUpdates()
sprite_path = pygame.sprite.OrderedUpdates()

def draw(surf, color, pos): 
    r = pygame.Rect(pos)
    pygame.draw.rect(surf, color, r)

def time():
    time = pygame.time.get_ticks()
    return time

def vector(travelx, travely, spx , spy):
    milli = clock.tick()
    seconds = 1/120.
    dmx = seconds * spx
    dmy = seconds * spy
    x = dmx + travelx
    y = dmy + travely
    print("vector")
    return x, y

def loadImage(fileName, useColorKey=False):
    filePath = os.path.join(game_assets, fileName)
    if os.path.isfile(filePath):
        image = pygame.image.load(filePath)
        image = image.convert_alpha()
        return image # Send image back
    else:
        raise Exception("Failed to load image: " + filePath + " - Incorrect path?")

grass_terrain = loadImage("Terrain\GrassBiome\Animated Tiles\GB-GrassLand-Coast-Animated.png")
road_terrain = loadImage("Terrain\DirtBiome\Animated Tiles\DB-Rock-Coast-Animated.png")
deer_sprite = []
for state in range(4):
    for frame in range(4):
        if state == 0:
            deer_sprite.append(loadImage("Creatures\Rampart\Deer\DeerWalk(Frame " + str(frame + 1) +").png"))
        elif state == 1:
            deer_sprite.append(loadImage("Creatures\Rampart\Deer\DeerDeath(Frame " + str(frame + 1) +").png"))
        elif state == 2:
            deer_sprite.append(loadImage("Creatures\Rampart\Deer\DeerHit(Frame " + str(frame + 1) +").png"))
        else:
            deer_sprite.append(loadImage("Creatures\Rampart\Deer\DeerAttack(Frame " + str(frame + 1) +").png"))



class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename, framesx = 1, framesy = 1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        #img  = loadImage(filename)
        img = filename
        #posx = i%grid_col
        #posy = (i//grid_col)
        self.originalWidth = img.get_width() // framesx # gets number of frames from sheet
        self.originalHeight = img.get_height() //framesy # gets number of frames from sheet

        frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        x = 0
        y = 0
        for frameNoy in range(framesy):
            for frameNox in range(framesx):
                x = -frameNox * self.originalWidth
                y = -frameNoy * self.originalHeight
                frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
                frameSurf.blit(img, (x, y))
                self.images.append(frameSurf.copy())

        #for frameNo in range(framessize):
        #    frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        #    frameSurf.blit(img, (x,0))
        #    self.images.append(frameSurf.copy())
        #    x -= self.originalWidth
        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
    
    def addImage(self, filename):
        #self.images.append(loadImage(filename))
        self.images.append(filename)

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)
        

    