# NEOS (Neuro Evolution Organism Simulator) by Edward Ng
#
# Evolution simulator using NEAT algorithm. Tries to observe a population
# of simple organisms (NEOS) learning to eat food. The NEOS can reproduce
# within a generation to create offspring of shared genes. By the end of 
# each generation sim, the fittest NEOS will carry the genes 
# for the next generation.
# 4/17/2023

from NEOS import *
from food import *
from evo_sim import *
from utils import *

from random import randint

settings = {}

# Evolution Settings
settings['pop_size'] = 64       # initial number of organisms
settings['food_num'] = 100      # number of food particles
settings['gens'] = 10            # number of generations
settings['elitism'] = 0.20      # elitism (selection bias)
settings['mutate'] = 0.10       # mutation rate
settings['mature'] = 200        # time for organism to mature (in total time steps)
settings['lifespan_lower'] = 500      # starting lifespan lower bound (in total time steps)
settings['lifespan_upper'] = 600      # starting lifespan upper bound (in total time steps)

# Simulation Setitngs
settings['gen_time'] = 50       # generation length         (seconds)
settings['dt'] = 0.04           # simulation time step      (dt)

settings['total_time_steps'] = int(settings['gen_time'] / settings['dt']) # total time steps of simulation (1250)

settings['dr_max'] = 720        # max rotational speed      (degrees per second)
settings['v_max'] = 0.5         # max velocity              (units per second)
settings['dv_max'] =  0.25      # max acceleration (+/-)    (units per second^2)

settings['x_min'] = -2.0        # experiment western border
settings['x_max'] =  2.0        # experiment eastern border
settings['y_min'] = -2.0        # experiment southern border
settings['y_max'] =  2.0        # experiment northern border

# Organism Neural Net Settings
settings['inner_nodes'] = 1          # number of input nodes
settings['hidden_nodes'] = 5          # number of hidden nodes
settings['outer_nodes'] = 2          # number of output nodes


def main(settings: dict) -> None:
    '''
    Run simulation which displays stats and saves the animation of the simulation.
    '''
    # init food to the environment
    foods = []
    for i in range(0,settings['food_num']):
        foods.append(food(settings))

    # init organisms to the environemnt
    organisms = []
    for i in range(0,settings['pop_size']):
        wih_init = np.random.uniform(-1, 1, (settings['hidden_nodes'], settings['inner_nodes']))     # mlp weights (input -> hidden)
        who_init = np.random.uniform(-1, 1, (settings['outer_nodes'], settings['hidden_nodes']))     # mlp weights (hidden -> output)

        lifespan = randint(settings['lifespan_lower'], settings['lifespan_upper']) 
        organisms.append(NEOS(settings, 'lightgreen', lifespan, None, None, wih_init, who_init, name='gen[0]-org['+str(i)+']', gen=0))

    # Loop through each generation
    for gen in range(0, settings['gens']):

        # simulation
        print("SIMULATING GEN "+str(gen)+". PLEASE WAIT...")

        fig, ax = plt.subplots()
        fig.set_size_inches(9.6, 5.4)
        ax.set_facecolor(plt.cm.Blues(.2))
        
        organisms, old_organisms = simulate(settings, organisms, foods, gen, fig, ax)

        
        # print stats
        stats = get_stats(organisms, old_organisms)
        print('> GEN:',gen,'BEST:',stats['BEST'],'AVG:',stats['AVG'],'WORST:',stats['WORST'],'SURVIVED:',stats['SURVIVED'],'DIED:',stats['DIED'],'TOTAL NEOS:',stats['COUNT'],'FOOD EATEN:',stats['SUM'])

        # organisms died off
        if len(organisms) == 0:
            print("DONE SIMULATING GEN "+str(gen)+".\n")
            break

        # add next generation of organisms
        organisms = evolve_gen(settings, organisms, gen)

        print("DONE SIMULATING GEN "+str(gen)+".\n")


if __name__ == "__main__":
    main(settings)
