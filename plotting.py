from matplotlib.patches import Circle
import matplotlib.lines as lines
from matplotlib import pyplot as plt

from NEOS import *

from math import sin
from math import cos
from math import radians

def plot_organism(x1, y1, theta, color, ax):
    '''
    Plot organisms on to the frame.
    :param x1:
    :param y1:
    :param theta:
    :param color:
    :param ax:
    :return: None
    '''
    circle = Circle([x1,y1], 0.05, edgecolor = 'g', facecolor = color, zorder=8)
    ax.add_artist(circle)

    edge = Circle([x1,y1], 0.05, facecolor='None', edgecolor = 'darkgreen', zorder=8)
    ax.add_artist(edge)

    tail_len = 0.075
    
    x2 = cos(radians(theta)) * tail_len + x1
    y2 = sin(radians(theta)) * tail_len + y1

    ax.add_line(lines.Line2D([x1,x2],[y1,y2], color='darkgreen', linewidth=1, zorder=10))



def plot_food(x1, y1, ax):
    '''
    Plot food particles on to the frame.
    :param x1:
    :param y1:
    :param ax:
    :return: None
    '''
    circle = Circle([x1,y1], 0.03, edgecolor = 'darkslateblue', facecolor = 'mediumslateblue', zorder=5)
    ax.add_artist(circle)
    



def plot_frame(settings, organisms, foods, gen, ax):
    '''
    Plot frame.
    :param settings:
    :param organisms:
    :param foods:
    :param gen:
    :param ax:
    :return: None
    '''
    plt.xlim([settings['x_min'] + settings['x_min'] * 0.25, settings['x_max'] + settings['x_max'] * 0.25])
    plt.ylim([settings['y_min'] + settings['y_min'] * 0.25, settings['y_max'] + settings['y_max'] * 0.25])

    # Plot organisms
    for organism in organisms:
        plot_organism(organism.x, organism.y, organism.r, organism.color, ax)

    # Plot food particles
    for food in foods:
        plot_food(food.x, food.y, ax)

    ax.set_aspect('equal')
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])

    plt.title(r'GENERATION: '+str(gen))
