from enum import IntEnum
import random 
import warnings 

class DEPLOYMENTS(IntEnum):
    NONE = 0
    HELI = 1
    FIREFIGHTER = 2
    FIRELINE = 3

    @staticmethod
    def print():
        for deployment in DEPLOYMENTS:
            print('{0} -> {1}'.format(deployment.value, deployment.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(DEPLOYMENTS))
    
    @staticmethod
    def get_value_from_string(deployment):
        for dep in DEPLOYMENTS:
            if deployment.upper() == dep.name:
                return dep.value
        else:
            warnings.warn('Tried to convert string ({}) to DEPLOYMENTS enum and failed; returned NONE'.format(deployment))
            return DEPLOYMENTS.NONE.value

    @staticmethod
    def get_name_from_string(deployment):
        for dep in DEPLOYMENTS:
            if deployment.upper() == dep.name:
                return dep.name
        else:
            warnings.warn('Tried to convert string ({}) to DEPLOYMENTS enum and failed; returned NONE'.format(deployment))
            return DEPLOYMENTS.NONE.name

class FIRELINE_DIRECTIONS(IntEnum):
    N = 0
    S = 1
    E = 2
    W = 3

    @staticmethod
    def print():
        for location in FIRELINE_DIRECTIONS:
            print('{0} -> {1}'.format(location.value, location.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(FIRELINE_DIRECTIONS))

    @staticmethod
    def get_value_from_string(location):
        for loc in FIRELINE_DIRECTIONS:
            if location.upper() == loc.name:
                return loc.value
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned N'.format(location))
            return FIRELINE_DIRECTIONS.N.value

    @staticmethod
    def get_name_from_string(location):
        for loc in FIRELINE_DIRECTIONS:
            if location.upper() == loc.name:
                return loc.name
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned N'.format(location))
            return FIRELINE_DIRECTIONS.N.name