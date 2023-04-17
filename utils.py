from math import atan2
from math import degrees
from math import sqrt
from math import floor
from random import randint

from collections import defaultdict

def dist(x1: float, y1: float, x2: float, y2: float) -> float:
    '''
    Calculate distance.
    :param x1: x position of target 1
    :param y1: y position of target 1
    :param x2: x position of target 2
    :param y2: y position of target 2
    :returns: distance in float.
    '''
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def calc_heading(organism, food) -> float:
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


def pick_color(gen: int) -> str:
    '''
    Pick color for organism based on generation. Randomize color if generation exceeds mapping.
    :param gen: int of generation.
    :return: string of color picked.
    '''
    # colors map to 10 generations and an albino variant
    color_mapping = {-1: 'mintcream', 0: 'lightgreen', 1: 'seagreen', 2: 'darkgreen', 3: 'darkolivegreen', 4: 'peru', 5: 'lightcoral', 6: 'orangered', 7: 'firebrick', 8: 'darkred', 9: 'black'}

    # chance of albino NEOS
    random_num = randint(0, 1000)
    if random_num == 5:
        return color_mapping[-1]

    if not gen in color_mapping:
        random_num = randint(0, 9)
        return color_mapping[random_num]
    return color_mapping[gen]
    

def boundary_fitness(organisms: list, percentage: float) -> int:
    '''
    Find boundary fitness rank for top percentile of organisms.
    :param organisms: list of organisms.
    :param percentage: the percentage of elite organisms.
    :return: Lowest fitness level of top organisms
    '''
    fitness_list = []
    for organism in organisms:
        fitness_list.append(organism.fitness)
    fitness_list.sort(reverse=True)
    idx = int(floor(len(fitness_list) * percentage)) - 1
    if idx < 0:
        return fitness_list[0]
    return fitness_list[idx]


def get_stats(organisms: list, old_organisms: list) -> dict:
    '''
    Get stats of simulation.
    '''
    # Get stats for current generation
    stats = defaultdict(int)

    stats['SURVIVED'] = len(organisms)
    stats['DIED'] = len(old_organisms)

    all_organisms = organisms + old_organisms
    for organism in all_organisms:
        if organism.fitness > stats['BEST'] or stats['BEST'] == 0:
            stats['BEST'] = organism.fitness

        if organism.fitness < stats['WORST'] or stats['WORST'] == 0:
            stats['WORST'] = organism.fitness

        stats['SUM'] += organism.fitness

    stats['COUNT'] = len(all_organisms)

    stats['AVG'] = stats['SUM'] / stats['COUNT']

    return stats
