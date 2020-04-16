import simpy

import world


def main():
    # Entire simulation process, must make all the data here available to the gui
    env = simpy.Environment()

    # simulating one (small) sample community for now
    boundaries = ((0, 10), (0, 10))  # boundaries for the sample community

    sample_community = world.Community(boundaries, env, no_of_people=10)
    sample_community.activate()

    # initially used env.step to run the environment, but that had a weird side effect
    # of not actually updating the environment time (env.now)
    for step in range(100):
        print("Step {}".format(step))
        env.run(until=env.now+1) # proceed by one time step

if __name__ == "__main__":
    main()
