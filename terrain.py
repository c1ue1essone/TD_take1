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