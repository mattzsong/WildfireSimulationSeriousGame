import numpy as np
import random
import math
from gym_wildfire_sim.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS, FIRELINE_DIRECTIONS
from gym_wildfire_sim.envs.enums.LOCATIONS import LOCATIONS


class Cell:

    def __init__(self, x_coord, y_coord, adj_locs, terrain):
        self.x = x_coord
        self.y = y_coord
        self.adj_locs = adj_locs
        self.terrain = terrain
        self.is_edge = False
        self.burning_percent = 0.0
        self.fmc = 0.0
        self.wind_velo = 0.0
        self.fuel_pack_ratio = 0.0
        self.theta = 0
        self.current_deployments = []
        self.archive_deployments = []
        self.firefighter_turn_counter = []
        self.fsr = 0.0

        self._init_values()

    def _init_values(self):
        self.wind_velo = self.terrain.base_wind_velo + \
            round(random.uniform(-2.5, 2.5),2)
        self.fuel_pack_ratio = self.terrain.base_packing_ratio + \
            round(random.uniform(-0.02, 0.02),4)
        self.theta = random.randrange(-45, 45)
        self._calculate_fmc()
        self._calculate_fsr()

    def update_values(self):
        self._calculate_fmc()
        self._calculate_fsr()
        self._check_edge()

    def add_deployment(self, deployment):
        self.current_deployments.append(deployment)
        self.archive_deployments.append(deployment)
        if deployment == DEPLOYMENTS.FIREFIGHTER:
            self.firefighter_turn_counter.append(1)

    def add_deployments(self, deployments):
        self.current_deployments.extend(deployments)
        self.archive_deployments.extend(deployments)

    def remove_deployment(self, deployment):
        self.current_deployments.remove(deployment)

    def remove_deployments(self, deployments):
        for d in deployments:
            if d in self.current_deployments:
                self.current_deployments.remove(d)

    def add_to_archives(self, dep):
        self.archive_deployments.append(dep)

    def get_current_deps(self):
        deps = self.current_deployments
        dep_values = []
        for dep in deps:
            dep_values.append(dep.value)
        return dep_values

    def destroy_deployments_by_type(self, dep_types):
        updated_deps = [
            dep for dep in self.current_deployments if dep not in dep_types]
        self.current_deployments = updated_deps

    def get_dep_history(self, deployment):
        return self.archive_deployments

    def _calculate_fsr(self):
        feet_min = (0.0002*pow(self.fmc, 2)-0.008 *
                    self.fmc+0.1225)*pow(self.wind_velo, 2)
        feet_min += (-0.0008*pow(self.fmc, 2)+0.0005 *
                     self.fmc+0.1823)*self.wind_velo
        feet_min += 0.0019*pow(self.fmc, 2)-0.0924*self.fmc+1.2675
        Ba = (0.0075*pow(self.theta, -0.196))*pow(self.wind_velo, 2) + (0.0002 *
                                                                        self.theta-0.0985)*self.wind_velo + 4.0767*pow(self.wind_velo, -0.429)
        Bs = 5.275*pow(self.fuel_pack_ratio, -0.3) * \
            pow(math.tan(self.theta), 2)
        feet_min *= Ba * (1+Bs)
        self.fsr = round(feet_min * 60 / 5280, 4)

    def _calculate_fmc(self):
        temp_index = int((self.terrain.temp-10)/20)
        humidity_index = int(self.terrain.humidity/5)
        self.fmc = self.terrain.FMC_TABLE[humidity_index][temp_index]

    def get_data(self):
        self.update_values()
        cell_values = {'x': self.x,
                       'y': self.y,
                       'is_edge': self.is_edge,
                       'burning_percent': self.burning_percent,
                       'fmc': self.fmc,
                       'wind_velo': self.wind_velo,
                       'theta': self.theta,
                       'fuel_pack_ratio': self.fuel_pack_ratio,
                       'fsr': self.fsr}
        return cell_values

    def _check_edge(self):
        edge = False
        for loc in self.adj_locs:
            if loc.burning_percent == 0:
                edge = True
                break
        self.is_edge = edge


if __name__ == '__main__':
    c = Cell(4, 4,(LOCATIONS.N, LOCATIONS.S, LOCATIONS.E, LOCATIONS.W))
    print(c.get_data)