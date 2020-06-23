

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