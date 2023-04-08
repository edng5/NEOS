from collections import defaultdict
import operator
from matplotlib.animation import PillowWriter

from NEOS import *
from food import *
from utils import *
from plotting import *

from math import floor
from random import randint
from random import random
from random import sample
from random import uniform

def evolve(settings: dict, organisms_old: list, gen: int) -> tuple:
    ''' 
    Evolve next generation of NEOS by crossing over genes
    and then mutating them.
    :param settings: contains dictionary of simulation config.
    :param organisms_old: contains a list of previous gen organisms.
    :param gen: integer of current generation.
    :returns: tuple of new organisms and statistics.
    '''
    elitism_num = int(floor(settings['elitism'] * settings['pop_size']))
    new_orgs = settings['pop_size'] - elitism_num

    # Get stats for current generation
    stats = defaultdict(int)
    for organism in organisms_old:
        if organism.fitness > stats['BEST'] or stats['BEST'] == 0:
            stats['BEST'] = organism.fitness

        if organism.fitness < stats['WORST'] or stats['WORST'] == 0:
            stats['WORST'] = organism.fitness

        stats['SUM'] += organism.fitness
        stats['COUNT'] += 1

    stats['AVG'] = stats['SUM'] / stats['COUNT']


    # Elitism (Keep the best performing organisms)
    orgs_sorted = sorted(organisms_old, key=operator.attrgetter('fitness'), reverse=True)
    organisms_new = []
    for i in range(0, elitism_num):
        organisms_new.append(NEOS(settings, wih=orgs_sorted[i].wih, who=orgs_sorted[i].who, name=orgs_sorted[i].name))


    # Generate new organisms
    for w in range(0, new_orgs):

        # Selection (Truncation Selection)
        candidates = range(0, elitism_num)
        random_index = sample(candidates, 2)
        org_1 = orgs_sorted[random_index[0]]
        org_2 = orgs_sorted[random_index[1]]

        # Crossover
        crossover_weight = random()
        wih_new = (crossover_weight * org_1.wih) + ((1 - crossover_weight) * org_2.wih)
        who_new = (crossover_weight * org_1.who) + ((1 - crossover_weight) * org_2.who)

        # Mutation
        mutate = random()
        if mutate <= settings['mutate']:

            # Pick which weight to mutate
            mat_pick = randint(0,1)

            # Mutate: WIH Weights
            if mat_pick == 0:
                index_row = randint(0,settings['hidden_nodes']-1)
                wih_new[index_row] = wih_new[index_row] * uniform(0.9, 1.1)
                if wih_new[index_row] >  1: wih_new[index_row] = 1
                if wih_new[index_row] < -1: wih_new[index_row] = -1

            # Mutate: WHO Weights
            if mat_pick == 1:
                index_row = randint(0,settings['outer_nodes']-1)
                index_col = randint(0,settings['hidden_nodes']-1)
                who_new[index_row][index_col] = who_new[index_row][index_col] * uniform(0.9, 1.1)
                if who_new[index_row][index_col] >  1: who_new[index_row][index_col] = 1
                if who_new[index_row][index_col] < -1: who_new[index_row][index_col] = -1

        # Mutate: Color
        color_new = pick_color(gen)

        organisms_new.append(NEOS(settings, color=color_new, wih=wih_new, who=who_new, name='gen['+str(gen)+']-org['+str(w)+']'))

    return organisms_new, stats


def simulate(settings: dict, organisms: list, foods: list, gen: int, fig, ax):
    ''' 
    Simulate current generation of NEOS through time steps and
    saving plot frames into an animation.
    :param settings: contains dictionary of simulation config.
    :param organisms: contains a list of organisms.
    :param foods: contains a list of foods.
    :param gen: integer of current generation.
    :param fig: plot figure.
    :param ax: plot ax.
    :returns: organisms
    '''
    metadata = dict(title='NEOS', artist='edng5')
    writer = PillowWriter(fps=15, metadata=metadata)

    
    total_time_steps = int(settings['gen_time'] / settings['dt'])

    # Save all frames into an animation
    with writer.saving(fig, 'gen_'+str(gen)+'.gif', 100):
        # Loop through the number of time steps
        
        for t_step in range(0, total_time_steps, 1):

            # Plot frames
            if settings['plot']==True: # and gen==settings['gens']-1:
                plot_frame(settings, organisms, foods, gen, ax)

            # Update fitness function
            for food in foods:
                for organism in organisms:
                    food_org_dist = dist(organism.x, organism.y, food.x, food.y)

                    # Update fitness function
                    if food_org_dist <= 0.075:
                        organism.fitness += food.energy
                        food.respawn(settings)

                    # Reset distance and heading to nearest food
                    organism.d_food = 100
                    organism.r_food = 0

            # Calculate heading to nearest food
            for food in foods:
                for organism in organisms:

                    # Calculate distance to selected food particle
                    food_org_dist = dist(organism.x, organism.y, food.x, food.y)

                    # Determine if this is the closest food particle
                    if food_org_dist < organism.d_food:
                        organism.d_food = food_org_dist
                        organism.r_food = calc_heading(organism, food)

            # Get organism response
            for organism in organisms:
                organism.think()

            # Update organisms position and velocity
            for organism in organisms:
                organism.update_r(settings)
                organism.update_vel(settings)
                organism.update_pos(settings)

            # Grab current plot to compile into an animation
            writer.grab_frame()
            ax.clear()
            ax.set_facecolor(plt.cm.Blues(.2))

    return organisms
