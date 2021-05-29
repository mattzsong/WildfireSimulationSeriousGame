import gym 
from gym import spaces
import math
from gym_wildfire_sim.envs.model.Terrain import Terrain
from gym_wildfire_sim.envs.enums.NATURE_STATES import WIND_STATES, PACKING_RATIO_STATES
from gym_wildfire_sim.envs.enums.LOCATIONS import LOCATIONS
from gym_wildfire_sim.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS, FIRELINE_DIRECTIONS
from gym_wildfire_sim.envs.enums.PLAY_TYPE import PLAY_TYPE

class WildfireSim(gym.Env):

    def __init__(self):
        self.play_type = PLAY_TYPE.MACHINE
        self.render_mode = 'machine'

        self.MAX_TURNS = 24

        self.terrain = Terrain()
        self.total_score = 0
        self.turn = 0
        self.done = False
        self._num_locations = 81
        self._num_deployments = len(DEPLOYMENTS)
        self._num_actions = self._num_locations * self._num_deployments
        self.action_space = spaces.Discrete(self._num_actions)
        self.observation_space = spaces.Box(low = 0, high = 100.0, shape = (82, max(6, 2+self.max_turns)), dtype='float32')
        self.reset()

    def reset(self):
        self.terrain = Terrain()
        self.total_score = 0
        self.turn = 0
        self.done = False
        self._num_locations = 81
        self._num_deployments = len(DEPLOYMENTS)
        self._num_actions = self._num_locations * self._num_deployments
        self.action_space = spaces.Discrete(self._num_actions)
        self.observation_space = spaces.Box(low = 0, high = 100.0, shape = (82, max(6, 2+self.max_turns)), dtype='float32')
        obs = self.get_obs()
        return obs

    def step(self, action):
        formatted_action = self.decode_raw_action(action=action)
        score, done = self._do_turn(formatted_action)
        self.total_score += score
        self.turn += 1
        if done or (self.turn >= self.MAX_TURNS):
            self.done = True
        obs = self.get_obs()
        info = {'turn': self.turn, 'step_reward': score, 'total_reward': self.total_score}
        return obs, self.total_score, self.done, info

    def _do_turn(self, action):
        score, done = self.terrain.do_turn(action=action)
        return score, done
    
    def get_obs(self):
        if self.play_type == PLAY_TYPE.HUMAN:
            return self.city.human_encode()
        elif self.play_type == PLAY_TYPE.MACHINE:
            return self.city.rl_encode()
        else:
            raise ValueError('Failed to find acceptable play type.')

    def render(self, mode='human'):
        if self.render_mode == 'human' or mode == 'human':
            return self.city.human_render()
        elif self.render_mode == 'machine' or mode == 'machine':
            return self.city.rl_render()
        else:
            raise ValueError('Failed to find acceptable play type.')

    @staticmethod
    def encode_raw_action(x, y, deployment):
        action = (x*9+y)*len(DEPLOYMENTS) + deployment.value
        return action

    @staticmethod
    def decode_raw_action(action):
        readable_action = []
        location_int = action // len(DEPLOYMENTS)
        deployment_int = action % len(DEPLOYMENTS)
        x = location_int // 9
        y = location_int % 9
        readable_action.extend(x, y, deployment_int)
        return readable_action

    