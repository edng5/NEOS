# NEOS (Neuro Evolution Organism Simulator) by Edward Ng
#
# Evolution simulator using NEAT algorithm. Tries to observe a population
# of simple organisms (NEOS) learning to eat food. The fittest of the generation
# will carry genes for the next generation.
# 4/2/2023

from NEOS import *
from food import *
from evo_sim import *
from utils import *

settings = {}

# Evolution Settings
settings['pop_size'] = 50       # number of organisms
settings['food_num'] = 100      # number of food particles
settings['gens'] = 10           # number of generations 50
settings['elitism'] = 0.20      # elitism (selection bias)
settings['mutate'] = 0.10       # mutation rate

# Simulation Setitngs
settings['gen_time'] = 50       # generation length         (seconds) 100
settings['dt'] = 0.04           # simulation time step      (dt)
settings['dr_max'] = 720        # max rotational speed      (degrees per second)
settings['v_max'] = 0.5         # max velocity              (units per second)
settings['dv_max'] =  0.25      # max acceleration (+/-)    (units per second^2)

settings['x_min'] = -2.0        # experiment western border
settings['x_max'] =  2.0        # experiment eastern border
settings['y_min'] = -2.0        # experiment southern border
settings['y_max'] =  2.0        # experiment northern border

settings['plot'] = True        # plot final generation?

# Organism Neural Net Settings
settings['inner_nodes'] = 1          # number of input nodes
settings['hidden_nodes'] = 5          # number of hidden nodes
settings['outer_nodes'] = 2          # number of output nodes


def main(settings: dict) -> None:
    '''Run simulation which displays stats and saves the animation of the simulation.
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

        organisms.append(NEOS(settings, 'lightgreen', wih_init, who_init, name='gen[x]-org['+str(i)+']'))

    # Loop through each generation
    for gen in range(0, settings['gens']):

        # simulation
        fig, ax = plt.subplots()
        fig.set_size_inches(9.6, 5.4)
        ax.set_facecolor(plt.cm.Blues(.2))
        organisms = simulate(settings, organisms, foods, gen, fig, ax)

        # add next generation of organisms
        organisms, stats = evolve(settings, organisms, gen)
        print('> GEN:',gen,'BEST:',stats['BEST'],'AVG:',stats['AVG'],'WORST:',stats['WORST'])


if __name__ == "__main__":
    main(settings)