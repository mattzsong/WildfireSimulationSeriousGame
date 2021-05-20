from enum import IntEnum
import random
import warnings

class WIND_STATES(IntEnum):
    CALM = 0
    MODERATE = 1
    STRONG = 2
    GALE = 3

    @staticmethod
    def print():
        for wind_state in WIND_STATES:
            print('{0} -> {1}'.format(wind_state.value, wind_state.name))

    @staticmethod
    def get_random():
        templist = list(WIND_STATES)
        temp = random.choice(templist)
        return temp
    
    @staticmethod
    def get_value_from_string(state):
        if state.upper() in [s.name for s in WIND_STATES]:
            exec('return WIND_STATES.' + state.upper() + '.value')
        else:
            warnings.warn('Tried to convert string ({}) to WIND_STATES enum and failed; returned CALM'.format(state))
            return WIND_STATES.CALM.value

    @staticmethod 
    def get_name_from_string(state):
        if state.upper() in [s.name for s in WIND_STATES]:
            exec('return WIND_STATES.' + state.upper() + '.name')
        else:
            warnings.warn('Tried to convert string ({}) to WIND_STATES enum and failed; returned CALM'.format(state))
            return WIND_STATES.CALM.name

class PACKING_RATIO_STATES(IntEnum):
    SPARSE = 0
    DENSE = 1

    @staticmethod
    def print():
        for packing_ratio_state in PACKING_RATIO_STATES:
            print('{0} -> {1}'.format(packing_ratio_state.value, packing_ratio_state.name))

    @staticmethod
    def get_random():
        templist = list(PACKING_RATIO_STATES)
        temp = random.choice(templist)
        return temp
    
    @staticmethod
    def get_value_from_string(state):
        if state.upper() in [s.name for s in PACKING_RATIO_STATES]:
            exec('return PACKING_RATIO_STATES.' + state.upper() + '.value')
        else:
            warnings.warn('Tried to convert string ({}) to PACKING_RATIO_STATES enum and failed; returned SPARSE'.format(state))
            return PACKING_RATIO_STATES.SPARSE.value

    @staticmethod 
    def get_name_from_string(state):
        if state.upper() in [s.name for s in PACKING_RATIO_STATES]:
            exec('return PACKING_RATIO_STATES.' + state.upper() + '.name')
        else:
            warnings.warn('Tried to convert string ({}) to PACKING_RATIO_STATES enum and failed; returned SPARSE'.format(state))
            return PACKING_RATIO_STATES.SPARSE.name
    
