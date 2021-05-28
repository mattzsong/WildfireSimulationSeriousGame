from enum import IntEnum
import random
import warnings
class LOCATIONS(IntEnum):
    N = 0
    S = 1
    E = 2
    W = 3
    @staticmethod
    def print():
        for location in LOCATIONS:
            print('{0} -> {1}'.format(location.value, location.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(LOCATIONS))

    @staticmethod
    def get_value_from_string(location):
        for loc in LOCATIONS:
            if location.upper() == loc.name:
                return loc.value
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned CENTER'.format(location))
            return LOCATIONS.CENTER.value

    @staticmethod
    def get_name_from_string(location):
        for loc in LOCATIONS:
            if location.upper() == loc.name:
                return loc.name
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned CENTER'.format(location))
            return LOCATIONS.CENTER.name