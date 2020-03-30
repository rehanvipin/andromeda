import random


class Person:
    """ A person in our simulation model, these objects live the box models. 
        They need these properties:
        1. Which box they belong to, given at init (Not needed?)
        2. Location within the box, also given at init
        3. Infected state , false at init
        4. Time since infection. (Needs to be handled by simpy)
    """

    def __init__(self, start_pos):
        self.position = start_pos
        self.infected = False
        self.time_infected = -1     # Invalid means not infected
        self.walk_range = 3
    
    def wander(self, boundaries):
        """ The random walk the particle will be doing till the end of the simulation.
            This doesn't have to be a class method, but will be convenient.
            The particle will wander in the boundaries.
            Need to define per call shift range. i.e how much movement per step
        """
        (start_x, end_x), (start_y, end_y) = boundaries
        cur_x, cur_y = self.position
        new_x = random.randrange(0,self.walk_range) + cur_x
        new_y = random.randrange(0,self.walk_range) + cur_y
        # Try to move within the correct boundaries
        while not (start_x <= new_x <= end) and not (start_y <= new_y <= end_y):
            new_x = random.randrange(0,self.walk_range) + cur_x
            new_y = random.randrange(0,self.walk_range) + cur_y
        self.position = new_x, new_y

        # This is not the final function ofc, need to also consider the factor of other 
        # points being in the way, and physical distancing.


class Community:
    """ A community in our model world, they are represented by boxes.
        There are also isolation communities. They are rendered on the 'Canvas'
        The particles move around within the boundaries of the box. In some rare cases
        they are allowed to travel(and spread the virus, what fun!)
        The properties these objects need to have are:
        1. The people in the communites, can be a list
        2. Position within the canvas
        3. Lockdown?
    """

    def __init__(self, position, no_of_people=60):
        self.position = position
        self.popultaion = []
        (start_x, end_x), (start_y, end_y) = position
        for _ in range(no_of_people):
            start_pos = (random.randrange(start_x, end_x), random.randrange(start_y, end_y))
            self.popultaion.append(Person(start_pos))
    
    def activate(self, iterations):
        """ Activate the community for this much time, i.e. the particles are active 
            in this time period and move around randomly. Maybe this should be infinite,
            maybe this should be parallelized with threads, thoughts for a later day.
        """
        boundaries = self.position
        for time_count in iterations:
            for person in self.position:
                person.wander(boundaries)
                # Render
        