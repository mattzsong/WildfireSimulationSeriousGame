import numpy as np
import json
import random

class Terrain:
    
    def __init__(self, config_file = 'config.json'):
        self.FILENAME = config_file
        
        self.cells = []
        self.temperature = 0
        self.humidity = 0
        self.wind_dir = []
        
        self.num_cells = 0

    def _init_config(self, filename):
        with open(filename) as file:
            data = json.load(file)
        self.temperature = data[]
    def 
