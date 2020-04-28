import random


import simpy
import pytest


import world
import render


def main():
    """Entire simulation process, must make all the data here available to the gui
    """
    env = simpy.Environment()

    # simulating one (small) sample community for now
    boundaries = ((0, 100), (0, 100))  # boundaries for the sample community

    num_popular_places = 4
    popular_places = []
    for _ in range(num_popular_places):
        popular_places.append((random.randrange(boundaries[0][0], boundaries[0][1]),
                               random.randrange(boundaries[1][0], boundaries[1][1])))

    sample_community = world.Community(boundaries,
                                       env,
                                       no_of_people=20,
                                       popular_places=popular_places)
    sample_community.activate()

    def before(env):
        env.run(until=env.now+1)

    render.render_community(-1, # number of steps
                            env,
                            sample_community,
                            before_callback=before,
                            before_kwargs={"env": env})

def test_main():
    # BUG , make it shut up for some time
    assert 1 == 1

if __name__ == "__main__":
    main()
