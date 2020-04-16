import random

import simpy

class Person:
    """ A person in our simulation model, these objects live the box models.
        They need these properties:
        1. Which box they belong to, given at init (Not needed?)
            1.1 Also a unique ID to identify them (probably not needed, but useful for debugging)
        2. Location within the box, also given at init
        3. Infected state, false at init
        4. Time since infection. (Needs to be handled by simpy)
        5. Boundaries of the box they are in (given at init)
    """

    def __init__(self, person_id, start_pos, boundaries, env: simpy.Environment):
        self.id_ = person_id
        self.position = start_pos
        self.infected = False
        self.time_infected = -1     # Invalid means not infected
        self.walk_range = 5
        self.walk_duration = 10 # max duration (in terms of simpy env steps) to walk for
        self.stop_duration = 10 # same as above, but for being in one place
        self.env = env # simpy environment
        self.boundaries = boundaries
        # self.process = env.process(self.activate())

    def activate(self):
        """Activates an infinite loop of walking and stopping
        """
        while True:
            yield self.env.process(self.wander())
            print("Person {} is at position {} at time {}".format(self.id_,
                                                                  self.position,
                                                                  self.env.now))
            yield self.env.timeout(random.randrange(self.stop_duration))

    def wander(self):
        """ The random walk the particle will be doing till the end of the simulation.
            This doesn't have to be a class method, but will be convenient.
            The particle will wander in the boundaries.
            Need to define per call shift range. i.e how much movement per step

            Times out for some time before actually updating the position.
            It would be better if it moved one position per time step, instead
            of teleporting to the location.
        """
        (start_x, end_x), (start_y, end_y) = self.boundaries
        cur_x, cur_y = self.position
        new_x = random.randrange(0, self.walk_range) + cur_x
        new_y = random.randrange(0, self.walk_range) + cur_y
        # Try to move within the correct boundaries
        while not (start_x <= new_x <= end_x) or not (start_y <= new_y <= end_y):
            new_x = random.randrange(-self.walk_range, self.walk_range+1) + cur_x
            new_y = random.randrange(-self.walk_range, self.walk_range+1) + cur_y

        def get_direction(position, target):
            if position < target:
                return 1
            if position > target:
                return -1
            return 0

        while cur_x != new_x or cur_y != new_y:
            direction = (get_direction(cur_x, new_x), get_direction(cur_y, new_y))
            cur_x += direction[0]
            cur_y += direction[1]
            self.position = cur_x, cur_y
            yield self.env.timeout(1)

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

    def __init__(self, position, env: simpy.Environment, no_of_people=60):
        self.position = position  # defines boundaries of the community
        self.env = env  # SimPy environment
        self.population = []
        (start_x, end_x), (start_y, end_y) = position
        for person_id in range(no_of_people):
            start_pos = (random.randrange(start_x, end_x), random.randrange(start_y, end_y))
            self.population.append(Person(person_id, start_pos, position, env))
        self.population_processes = []  # to store the SimPy processes for each person
        # ^ this could be dict

    def get_all_positions_x_y(self):
        """Get positions of all people in the form of two separate x and y lists.
        This is a helper function for plotting.
        """
        x = []
        y = []
        for person in self.population:
            x.append(person.position[0])
            y.append(person.position[1])
        return x, y

    def set_people_attribute(self, attr_name, value):
        """Sets an attribute for all people in the population"""
        for person in self.population:
            setattr(person, attr_name, value)

    def activate(self):
        """Activates all the people in this community. This will not lock the thread.
        """
        for person in self.population:
            self.population_processes.append(self.env.process(person.activate()))
        return self.population_processes
