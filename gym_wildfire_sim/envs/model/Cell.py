import numpy as np
import random
class Cell:

    def __init__(self, x_coord, y_coord, adj_locs, terrain):
        self.x = x_coord
        self.y = y_coord
        self.adj_locs = adj_locs
        self.terrain = terrain
        self.burning_percent = 0
        self.fmc = 0
        self.wind_velo = self.terrain.velocity + random.randrange(0, 5)
        self.fuel_pack_ratio = 0
        self.theta = 0
        self.deployments = []

    def calculate_fsr(self):

    def 
        

