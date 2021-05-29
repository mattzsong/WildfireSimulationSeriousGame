import numpy as np
import math
import json
import random
from gym_wildfire_sim.envs.model.Cell import Cell
from gym_wildfire_sim.envs.enums.NATURE_STATES import WIND_STATES, PACKING_RATIO_STATES
from gym_wildfire_sim.envs.enums.LOCATIONS import LOCATIONS
from gym_wildfire_sim.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS, FIRELINE_DIRECTIONS


class Terrain:

    def __init__(self, base_values, config_file='config.json'):
        self.FILENAME = config_file

        self.cells = []
        self.temp = 0
        self.humidity = 0
        self.base_wind_velo = 0.0
        self.base_packing_ratio = 0.0
        self.wind_dir = ()
        self.FMC_TABLE = ((1, 1, 1, 1, 1, 1), (2, 2, 2, 1, 1, 1), (2, 2, 2, 2, 2, 2), (3, 3, 3, 2, 2, 2), (4, 4, 4, 3, 3, 3),
                          (5, 5, 5, 4, 4, 4), (5, 5, 5, 5, 4, 4), (6, 6, 6,
                                                                   5, 5, 5), (7, 7, 6, 6, 6, 6), (8, 7, 7, 7, 7, 7),
                          (8, 8, 8, 8, 8, 8), (9, 9, 8, 8, 8, 8), (10, 10, 9, 9, 9,
                                                                   9), (11, 10, 10, 10, 10, 10), (12, 11, 11, 10, 10, 10),
                          (12, 12, 12, 11, 11, 11), (13, 13, 12, 12, 12, 12), (13, 13, 12, 12, 12, 12), (14, 13, 13, 13, 12))
        self.score = 0.0
        self.total_score = 0.0
        self.turn = 0
        self.max_turns = 24
        self.num_cells = 0

        self.BURNING_PERCENT_WEIGHTS = {}
        self.BASE_VALUES = {}

        self._init_config(self.FILENAME)
        self._init_base_values()
        self._init_cells()

    def _init_config(self, filename):
        with open(filename) as file:
            data = json.load(file)
        self.BURNING_PERCENT_WEIGHTS.update(data['burning_percent_weights'])
        self.BASE_VALUES.update(data['base_values'])

    def _init_base_values(self):
        self.temp = self.BASE_VALUES.get('TEMP')
        self.humidity = self.BASE_VALUES.get('HUMIDITY')
        self._init_wind(self.BASE_VALUES.get('WIND'))
        self._init_wind_dir()
        self._init_packing_ratio(self.BASE_VALUES.get('PACKING_RATIO'))

    def _init_wind_dir(self):
        horizontal = round(random.random()*2 - 1, 2)
        vertical = round(math.sqrt(1-pow(horizontal, 2)), 2)
        vertical *= -1 if random.random() >= 0.5 else 1
        self.wind_dir = (horizontal, vertical)

    def _init_wind(self, wind_profile):
        if wind_profile == WIND_STATES.CALM:
            self.base_wind_velo = round(random.uniform(2.5, 12), 2)
        elif wind_profile == WIND_STATES.MODERATE:
            self.base_wind_velo = round(random.uniform(12, 24), 2)
        elif wind_profile == WIND_STATES.STRONG:
            self.base_wind_velo == round(random.uniform(24, 36), 2)
        elif wind_profile == WIND_STATES.GALE:
            self.base_wind_velo == round(random.uniform(36, 46.5), 2)

    def _init_packing_ratio(self, packing_ratio_profile):
        if packing_ratio_profile == PACKING_RATIO_STATES.SPARSE:
            self.base_packing_ratio = round(random.uniform(0.08, 0.17), 4)
        elif packing_ratio_profile == PACKING_RATIO_STATES.DENSE:
            self.base_packing_ratio = round(random.uniform(0.17, 0.26), 4)

    def _init_cells(self):
        for x in range(9):
            cells.append([])
            for y in range(9):
                locations = [LOCATIONS.N, LOCATIONS.S,
                             LOCATIONS.E, LOCATIONS.W]
                if x == 0:
                    locations.remove(LOCATIONS.N)
                elif x == 8:
                    locations.remove(LOCATIONS.S)
                if y == 0:
                    locations.remove(LOCATIONS.W)
                elif y == 8:
                    locations.remove(LOCATIONS.E)
            cells[x].append(Cell(x, y, locations, self))

    def do_turn(self, action):
        x = action[0]
        y = action[1]
        dep = action[2]
        self.add_action_to_location(x, y, dep)
        self.adjust_burning_percents()
        self.process_action()
        self.remove_deployments()
        self.update_values()
        done = self.check_done()
        score = self.get_score()
        self.score = score
        self.total_score += score
        self.turn += 1
        self._update_firefighter_turns()

        return score, done

    def add_action_to_location(self, x, y, dep):
        if dep == DEPLOYMENTS.FIREFIGHTER:
            if self.cells[x][y].is_edge:
                self.cells[x][y].add_deployment(dep)
        elif dep == DEPLOYMENTS.FIRELINE:
            if self.cells[x][y].burning_percent == 0:
                self.cells[x][y].add_deployment(dep)
        elif dep != DEPLOYMENTS.NONE:
            self.cells[x][y].add_deployment(dep)

    def adjust_burning_percents(self):
        for x in range(9):
            for y in range(9):
                cell = self.cells[x][y]
                for dep in cell.current_deployments:
                    if dep is not DEPLOYMENTS.FIRELINE:
                        cell.burning_percent -= self.BURNING_PERCENT_WEIGHTS.get(
                            dep.name)
                cell.burning_percent = cell.burning_percent if cell.burning_percent > 0.0 else 0.0

    def process_action(self):
        for x in range(9):
            for y in range(9):
                cell = self.cells[x][y]
                horizontal, vertical = self._calculate_spread(cell)
                if horizontal < 0 and LOCATIONS.W in cell.adj_locs:
                    self.cells[x-1][y].burning_percent += horizontal
                    self.cells[x-1][y].burning_percent = self.cells[x-1][y].burning_percent if self.cells[x-1][y] <= 1.00 else 1.00
                if horizontal > 0 and LOCATIONS.E in cell.adj_locs:
                    self.cells[x+1][y].burning_percent += horizontal
                    self.cells[x+1][y].burning_percent = self.cells[x+1][y].burning_percent if self.cells[x+1][y] <= 1.00 else 1.00
                if vertical < 0 and LOCATIONS.S in cell.adj_locs:
                    self.cells[x][y+1].burning_percent += vertical
                    self.cells[x][y+1].burning_percent = self.cells[x][y+1].burning_percent if self.cells[x][y+1] <= 1.00 else 1.00
                if vertical > 0 and LOCATIONS.N in cell.adj_locs:
                    self.cells[x][y-1].burning_percent += vertical
                    self.cells[x][y-1].burning_percent = self.cells[x][y-1].burning_percent if self.cells[x][y-1] <= 1.00 else 1.00

            # check for a barrier on a cell and set burning_percent to 0
        for x in range(9):
            for y in range(9):
                if DEPLOYMENTS.FIRELINE in self.cells[x][y].current_deployments:
                    self.cells[x][y].burning_percent = 0

    def _calculate_spread(self, cell):
        horizontal = round(
            cell.fsr * self.wind_dir[0] * cell.burning_percent, 4)
        vertical = round(cell.fsr * self.wind_dir[1] * cell.burning_percent, 4)
        return horizontal, vertical

    def remove_deployments(self):
        for x in range(9):
            for y in range(9):
                self.cells[x][y].destroy_deployments_by_type(
                    [DEPLOYMENTS.HELI])
                self._check_firefighters(self.cells[x][y])

    def _check_firefighters(self, cell):
        to_remove = 0
        firefighter_index = 0
        for dep in cell.current_deployments:
            if dep == DEPLOYMENTS.FIREFIGHTER and cell.firefighter_turn_counter[firefighter_index] >= 8:
                to_remove += 1

        for _ in range(to_remove):
            cell.remove_deployment(DEPLOYMENTS.FIREFIGHTER)
            cell.firefighter_turn_counter.pop(0)

    def _update_firefighter_turns(self):
        for x in range(9):
            for y in range(9):
                for index in range(len(self.cells[x][y].firefighter_turn_counter)):
                    self.cells[x][y].firefighter_turn_counter[index] += 1

    def update_values(self):
        for x in range(9):
            for y in range(9):
                self.cells[x][y].update_values()

    def check_done(self):
        return self.turn > self.max_turns

    def get_score(self):
        score = 0
        for x in range(9):
            for y in range(9):
                score += self.cells[x][y].burning_percent
        score /= 8.1
        return score

    def human_encode(self):
        terrain_data = self.get_data()
        cells_data = []
        for x in range(9):
            for y in range(9):
                c_data = self.cells[x][y].get_data()
                cells_data.append(c_data)
        state_data = {'terrain': terrain_data, 'cells': cells_data}
        state_json = json.dumps(state_data)
        return state_json

    def rl_encode(self):
        
        state = np.zeros(shape = (82, max(6, 2+self.max_turns)), dtype='float32')

        #global values
        state[0,0] = self.temp #global temp
        state[0,1] = self.humidity #global humidity
        state[0,2] = self.base_wind_velo * self.wind_dir[0] #base horizontal wind
        state[0,3] = self.base_wind_velo * self.wind_dir[1] #base vertical wind
        state[0,4] = self.base_packing_ratio #global base packing ratio
        state[0,5] = self.score

        for x in range(9):
            for y in range(9):
                cell = self.cells[x][y]
                cell_data = cell.get_data()
                state[x*9+y+1, 0] = cell_data.get('burning_percent')
                state[x*9+y+1, 1] = cell_data.get('theta')
                for i in range(len(cell.current_deployments)):
                    state[x*9+y+1, i+2] = cell.current_deployments[i].value
                
    def rl_render(self):
        minimal_report = 'Turn {0} of {1}. Turn Score: {2}. Total Score: {3}'.format(self.turn, self.max_turns,
                                                                                     self.score, self.total_score)
        print(minimal_report)
        return minimal_report

    def get_data(self):
        self.update_values()
        terrain_values = {'temp': self.temp,
                          'humidity': self.humidity,
                          'score': self.get_score(),
                          'base_wind_velo': self.base_wind_velo,
                          'wind_dir': self.wind_dir,
                          'base_packing_ratio': self.base_packing_ratio}
        return terrain_values

if __name__ == '__main__':
    terrain = Terrain()
    print(terrain.get_data())
    
