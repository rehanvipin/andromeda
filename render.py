""" The graphical rendering part of the project
    Uses the values from the engine to describe the world.
    Still need to decide on the modules to be used.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, CheckButtons
import numpy as np

import world

def render_community(steps, env,
                     community: world.Community,
                     before_callback=None, before_args=None, before_kwargs=None,
                     after_callback=None, after_args=None, after_kwargs=None,
                     interval=100):
    """Renders a single community

        Parameters:
            - steps: Number of steps to run for. Use 0 or negative to simulate indefinitely
            - env: SimPy Environment (TODO: might not be required)
            - community: the community object to simulate
            - before_callback: a function to call before rendering each frame. Arguments to this
                function can be given using before_args and before_kwargs
            - after_callback: a function to call after rendering each frame. Arguments to this
                function can be given using after_args and after_kwargs
            - interval: time between each frame in ms
    """
    # initialize optional args here to avoid python quirks
    if not before_args:
        before_args = []
    if not after_args:
        after_args = []
    if not before_kwargs:
        before_kwargs = dict()
    if not after_kwargs:
        after_kwargs = dict()

    # if number of steps is negative or zero, run forever
    infinite = False
    if steps <= 0:
        infinite = True
        steps = None

    # make subplots, only 1 subplot since this function only simulates one community
    fig, ax = plt.subplots(1, 1)
    plt.subplots_adjust(left=0.25, bottom=0.25)
    ax.set_aspect('equal')
    ax.set_xlim(community.position[0][0]-2, community.position[0][1]+2)
    ax.set_ylim(community.position[1][0]-2, community.position[1][1]+2)

    # make axes for sliders and buttons
    axcolor = 'lightgoldenrodyellow'
    ax_slider_1 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    ax_slider_2 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    ax_left_1 = plt.axes([0.025, 0.5, 0.15, 0.05], facecolor=axcolor)

    # slider to control walk_range
    walk_range_slider = Slider(ax_slider_1, "Walk Range", 1, 20, valinit=5, valstep=1)
    # slider to control stop_duration
    stop_duration_slider = Slider(ax_slider_2, "Stop Duration", 1, 50, valinit=10, valstep=1)

    # common function to upload all sliders
    def update_sliders(_):
        community.set_people_attribute("walk_range", walk_range_slider.val)
        community.set_people_attribute("stop_duration", stop_duration_slider.val)
    # attach sliders to update function
    walk_range_slider.on_changed(update_sliders)
    stop_duration_slider.on_changed(update_sliders)

    num_people = len(community.population)

    # initialize the scatter plot
    x, y = community.get_all_positions_x_y()
    c = np.random.random((num_people)) # intialize random colors
    scat = ax.scatter(x, y, c=c, vmin=0, vmax=1,
                      cmap="jet", edgecolor="k")

    # utility function to update key-value args with local variables
    def change_kwargs(orig_kwargs, **kwargs):
        orig_kwargs.update(kwargs)

    def update(_):
        """Update the scatter plot."""

        # call the "before" function
        if before_callback:
            before_callback(*before_args, **before_kwargs)

        data = community.get_all_positions_x_y()
        # the scat.set_ functions need input in the form of numpy arrays
        data = np.array(data)

        # Set x and y data (input in the form of a 2D np array)
        scat.set_offsets(data[:2, :].T)
        # Set sizes of dots (we might not need this)
        # self.scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
        # Set colors of dots
        scat.set_array(c)

        # call the "after" function
        if after_callback:
            after_callback(*after_args, **after_args)

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return (scat, )

    anim = animation.FuncAnimation(fig, update, interval=interval,
                                   blit=True,
                                   repeat=infinite,
                                   frames=steps)

    anim_running = True # to keep track of the animation state

    def onClick(_):
        """Toggles between pause and resume of the animation"""
        nonlocal anim_running
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True
        ax.draw_artist(scat)

    # add a button widget to pause
    pause_button = CheckButtons(ax_left_1, ["Pause"])
    pause_button.on_clicked(onClick)
    # fig.canvas.mpl_connect('button_press_event', onClick)

    plt.show()

if __name__ == "__main__":
    pass
