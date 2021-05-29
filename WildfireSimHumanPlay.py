import json
import uuid
import gym
import gym_wildfire_sim
from gym_wildfire_sim.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS
from gym_wildfire_sim.envs.enums.PLAY_TYPE import PLAY_TYPE
from GUI import *
from gym_wildfire_sim.envs.model.Terrain import Terrain

class WildfireSim:

    def __init__(self, data_log_file='data_log.json'):
        self.ENV_NAME = 'WildfireSim'
        self.DATA_LOG_FILE_NAME = data_log_file
        self.GAME_ID = uuid.uuid4()
        self.env = None
        self.current_actions = []
        self.turn = 0
        self.max_turns = 24
        self._setup()

    def _setup(self):
        self.env = gym.make(self.ENV_NAME)
        self.env.play_type = PLAY_TYPE.HUMAN
        self.env.render_mode = 'human'
        self.env.MAX_TURNS = 24
        self.env.reset()
        print('Created new environment {0} with GameID: {1}'.format(self.ENV_NAME, self.GAME_ID))

    def done(self):
        print("Episode finished after {} turns".format(self.turn))
        self._cleanup()

    def _cleanup(self):
        self.env.close()

    def run(self):
        print('Starting new game with human play!')
        self.env.reset()
        
        for i in range(self.max_turns):
            print('Input Action - X Coordinate')
            x = input()
            print('Input Action - Y Coordinate')
            y = input()
            print('Input Action - Deployment')
            deployment = input()
            try:
                action = self.env.encode_raw_action(x = int(x), y = int(y), deployment = deployment)
            except:
                print('>>> Input error. Try again.')
                i -= 1
                continue
            else:
                print('>>> Input success.')

            observation, reward, done, info = self.env.step(action)
            print(info)
            self.env.render(mode='human')

            # Write action and stuff out to disk.
            data_to_log = {
                'game_id': str(self.GAME_ID),
                'step': self.turn,
                'action': action,
                'reward': reward,
                'game_done': done,
                'game_info': {k.replace('.', '_'): v for (k, v) in info.items()},
                'raw_state': observation
            }
            with open(self.DATA_LOG_FILE_NAME, 'a') as f_:
                f_.write(json.dumps(data_to_log) + '\n')

            # Update counter
            self.turn += 1
            if done:
                self.done()
                break