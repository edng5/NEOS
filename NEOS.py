import numpy as np

from utils import *

from math import atan2
from math import cos
from math import degrees
from math import floor
from math import radians
from math import sin
from math import sqrt
from random import uniform

class NEOS():
    '''
    Class for simple organisms called NEOS.
    '''
    def __init__(self, settings, color='lightgreen', lifespan=120, wih=None, who=None, name=None):

        self.x = uniform(settings['x_min'], settings['x_max'])  # position (x)
        self.y = uniform(settings['y_min'], settings['y_max'])  # position (y)

        self.r = uniform(0,360)                 # orientation   [0, 360]
        self.v = uniform(0,settings['v_max'])   # velocity      [0, v_max]
        self.dv = uniform(-settings['dv_max'], settings['dv_max'])   # dv

        self.d_food = 100   # distance to nearest food
        self.r_food = 0     # orientation to nearest food
        self.fitness = 0    # fitness (food count)
        self.color = color  # color
        self.age = 0        # age
        self.lifespan = lifespan # lifespan

        self.wih = wih
        self.who = who

        self.name = name


    def think(self) -> None:
        '''
        Neural Network of the organisms.
        :returns: None
        '''
        # MLP
        af = lambda x: np.tanh(x)               # activation function
        h1 = af(np.dot(self.wih, self.r_food))  # hidden layer
        out = af(np.dot(self.who, h1))          # output layer

        # Update dv and dr with MLP response
        self.nn_dv = float(out[0])   # [-1, 1]  (accelerate=1, deaccelerate=-1)
        self.nn_dr = float(out[1])   # [-1, 1]  (left=1, right=-1)


    def too_old(self) -> bool:
        '''
        Compare age with lifespan.
        :return: True if organism is too old.
        '''
        return self.age >= self.lifespan
    

    def update_r(self, settings: dict) -> None:
        '''
        Update the NEOS heading.
        :param settings: simulation configurations.
        :return: None
        '''
        self.r += self.nn_dr * settings['dr_max'] * settings['dt']
        self.r = self.r % 360


    def update_vel(self, settings: dict) -> None:
        '''
        Update the NEOS velocity.
        :param settings: simulation configurations.
        :return: None
        '''
        self.v += self.nn_dv * settings['dv_max'] * settings['dt']
        if self.v < 0: self.v = 0
        if self.v > settings['v_max']: self.v = settings['v_max']


    def update_pos(self, settings: dict) -> None:
        '''
        Update the NEOS position.
        :param settings: simulation configurations.
        :return: None
        '''
        dx = self.v * cos(radians(self.r)) * settings['dt']
        dy = self.v * sin(radians(self.r)) * settings['dt']
        self.x += dx
        self.y += dy


    def update_age(self) -> None:
        '''
        Update the NEOS age.
        :return: None
        '''
        self.age += 1
