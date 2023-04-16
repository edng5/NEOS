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

def evolve_gen(settings: dict, organisms_old: list, gen: int) -> list:
    ''' 
    Evolve next generation of NEOS by crossing over genes
    and then mutating them.
    :param settings: contains dictionary of simulation config.
    :param organisms_old: contains a list of previous gen organisms.
    :param gen: integer of current generation.
    :param count: number of organisms from previous gen.
    :param sum: number of food eaten from previous gen.
    :returns: list of new organisms.
    '''
    # Elitism (Keep the best performing organisms)
    elitism_num = int(floor(settings['elitism'] * len(organisms_old)))
    orgs_sorted = sorted(organisms_old, key=operator.attrgetter('fitness'), reverse=True)
    organisms_new = []

    for i in range(0, elitism_num):
        organisms_new.append(NEOS(settings, wih=orgs_sorted[i].wih, who=orgs_sorted[i].who, name=orgs_sorted[i].name))

    # Generate new organisms
    num_new_orgs = settings['pop_size'] - elitism_num
    for w in range(0, num_new_orgs):

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

        # Mutate: lifespan
        lifespan = randint(settings['lifespan_lower'], settings['lifespan_upper'])

        organisms_new.append(NEOS(settings, color=color_new, lifespan=lifespan, wih=wih_new, who=who_new, name='gen['+str(gen)+']-org['+str(w)+']'))

    return organisms_new


def reproduce(settings, organisms, organism1, organism2, gen, count) -> None:
    '''
    Reproduction of two organisms to create an organism with crossed 
    genes of the parents.
    :param settings: dictionary of simultation settings
    :param organisms: list of organisms 
    :param organism1: parent 1
    :param organism2: parent 2
    :param gen: current generation
    :param count: new organism count
    :return: None
    '''
    # Crossover
    crossover_weight = random()
    wih_new = (crossover_weight * organism1.wih) + ((1 - crossover_weight) * organism2.wih)
    who_new = (crossover_weight * organism1.who) + ((1 - crossover_weight) * organism2.who)

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

        # Mutate: lifespan
        lifespan = randint(settings['lifespan_lower'], settings['lifespan_upper'])

        organisms.append(NEOS(settings, color=color_new, lifespan=lifespan, wih=wih_new, who=who_new, name='gen['+str(gen)+']-org['+str(count)+']'))


def simulate(settings: dict, organisms: list, foods: list, gen: int, fig, ax) -> tuple:
    ''' 
    Simulate current generation of NEOS through time steps and
    saving plot frames into an animation.
    :param settings: contains dictionary of simulation config.
    :param organisms: contains a list of organisms.
    :param foods: contains a list of foods.
    :param gen: integer of current generation.
    :param fig: plot figure.
    :param ax: plot ax.
    :returns: list of organisms, list of organisms that died
    '''
    metadata = dict(title='NEOS', artist='edng5')
    writer = PillowWriter(fps=15, metadata=metadata)

    
    total_time_steps = settings['total_time_steps']
    old_organisms = []
    count = 0

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

            # Calculate fitness threshold
            threshold = boundary_fitness(organisms, settings['elitism'])

            # Calculate heading to nearest food
            for food in foods:
                for organism1 in organisms:
                    # Calculate distance to selected food particle
                    food_org_dist = dist(organism1.x, organism1.y, food.x, food.y)
                    for organism2 in organisms:
                        # determine to go to food or find mate
                        if organism1 != organism2:
                            # Calculate distance to selected organism
                            org_org_dist = dist(organism1.x, organism1.y, organism2.x, organism2.y)
                            if organism1.age > organism1.lifespan*0.75 and organism2.fitness > threshold and org_org_dist < organism1.d_org:
                                organism1.d_org = org_org_dist
                                organism1.r_org = calc_heading(organism1, organism2)
                            # Determine if this is the closest food particle
                            elif food_org_dist < organism1.d_food:
                                organism1.d_food = food_org_dist
                                organism1.r_food = calc_heading(organism1, food)

            # Organism reproduction
            for organism1 in organisms:
                for organism2 in organisms:
                    if organism1 != organism2:
                        org_org_dist = dist(organism1.x, organism1.y, organism2.x, organism2.y)

                        if org_org_dist <= 0.075:
                            if organism1.fitness > threshold and organism2.fitness > threshold and organism1.age > settings['mature'] and organism2.age > settings['mature']:
                                reproduce(settings, organisms, organism1, organism2, gen, count)
                                organism1.d_org = 100
                                organism1.r_org = 0
                                count += 1
            
            # Old age organisms die off
            for organism in organisms:
                if organism.too_old():
                    old_organisms.append(organism)
                    organisms.remove(organism)
                    count += 1

            # End simulation if all organisms are gone        
            if len(organisms) == 0:
                print("GEN "+str(gen)+" DID NOT SURVIVE...")
                break

            # Get organism response
            for organism in organisms:
                organism.think()

            # Update organisms position and velocity
            for organism in organisms:
                organism.update_r(settings)
                organism.update_vel(settings)
                organism.update_pos(settings)
                organism.update_age()


            # Too many NEOS
            if len(organisms) > 150:
                print("OVERPOPULATION - ENDING SIM...")
                break

            # Grab current plot to compile into an animation
            writer.grab_frame()
            ax.clear()
            ax.set_facecolor(plt.cm.Blues(.2))

    return organisms, old_organisms
