from math import atan2
from math import degrees
from math import sqrt
from random import randint

def dist(x1,y1,x2,y2):
    '''
    Calculate distance.
    :param x1:
    :param y1:
    :param x2:
    :param y2: 
    :returns: distance in float.
    '''
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def calc_heading(organism, food):
    '''
    Calculate the heading of organism to food
    particle.
    :param org: organism object.
    :param food: food object.
    :returns: heading in float.
    '''
    d_x = food.x - organism.x
    d_y = food.y - organism.y
    theta_d = degrees(atan2(d_y, d_x)) - organism.r
    if abs(theta_d) > 180: 
        theta_d += 360
    return theta_d / 180


def pick_color(gen):
    '''
    Pick color for organism based on generation. Randomize color if generation exceeds mapping.
    :param gen: int of generation.
    :return: string of color picked.
    '''
    color_mapping = {0: 'lightgreen', 1: 'forestgreen', 2: 'darkgreen', 3: 'mediumseagreen', 4: 'mediumaquamarine', 5: 'mintcream'}
    if not gen in color_mapping:
        random_num = randint(0, 5) #148
        return color_mapping[random_num]
    return color_mapping[gen]
    