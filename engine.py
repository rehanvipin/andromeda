import simpy

import world

import render


def main():
    # Entire simulation process, must make all the data here available to the gui
    env = simpy.Environment()

    # simulating one (small) sample community for now
    boundaries = ((0, 10), (0, 10))  # boundaries for the sample community

    sample_community = world.Community(boundaries, env, no_of_people=10)
    sample_community.activate()

    def before(env):
        env.run(until=env.now+1)

    render.render_community(-1, # number of steps
                            env,
                            sample_community,
                            before_callback=before,
                            before_kwargs={"env": env})

if __name__ == "__main__":
    main()
