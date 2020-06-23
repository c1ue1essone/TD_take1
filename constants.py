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

def draw(surf, color, pos): 
    r = pygame.Rect(pos)
    pygame.draw.rect(surf, color, r)

def vector(travelx, travely, spx , spy):
    milli = clock.tick()
    seconds = 1/120.
    dmx = seconds * spx
    dmy = seconds * spy
    x = dmx + travelx
    y = dmy + travely
    print("vector")
    return x, y