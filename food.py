from random import uniform

class food():
    '''
    Class for food particles.
    '''
    def __init__(self, settings):
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        self.energy = 1


    def respawn(self,settings: dict) -> None:
        '''
        Respawn food in random location within experiment boundaries.
        :param settings: simulation configurations.
        :returns: None
        '''
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        self.energy = 1
