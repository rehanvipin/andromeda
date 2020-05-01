""" The graphical rendering part of the project
    Uses the values from the engine to describe the world.
    Still need to decide on the modules to be used.
"""
import time
import math
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
    ax_slider_3 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
    ax_left_1 = plt.axes([0.025, 0.5, 0.15, 0.10], facecolor=axcolor)


    # For displaying framerate (doesn't work currently, can be reused for something else)
    # ax_left_2 = plt.axes([0.05, 0.8, 0.2, 0.05])
    # ax_left_2.get_xaxis().set_visible(False)
    # ax_left_2.get_yaxis().set_visible(False)
    # ax_left_2_bbox = ax_left_2.get_position(original=False).get_points()
    # fps_text_x = (ax_left_2_bbox[0][0] + ax_left_2_bbox[0][1]) / 2.0
    # fps_text_y = (ax_left_2_bbox[1][0] + ax_left_2_bbox[1][1]) / 2.0
    # fps_text = ax_left_2.text(fps_text_x, fps_text_y, "FPS", horizontalalignment='center', verticalalignment='center')

    max_walk_range = round(math.sqrt((community.position[0][1]-community.position[0][0])**2
                                     + (community.position[1][1]-community.position[1][0])**2))
    initial_walk_range = max_walk_range / 2
    community.set_people_attribute("walk_range", initial_walk_range)
    # slider to control walk_range
    walk_range_slider = Slider(ax_slider_1, "Walk Range", 1, max_walk_range, valinit=initial_walk_range, valstep=1)
    # slider to control stop_duration
    stop_duration_slider = Slider(ax_slider_2, "Stop Duration", 1, 200, valinit=10, valstep=1)
    # slider to control probability of going to a popular place
    pop_place_slider = Slider(ax_slider_3, "Prob of going to popular place", 0, 1, valinit=0.3)

    # common function to upload all sliders
    def update_sliders(_):
        community.set_people_attribute("walk_range", walk_range_slider.val)
        community.set_people_attribute("stop_duration", stop_duration_slider.val)
        community.set_people_attribute("popular_place_probability", pop_place_slider.val)
    # attach sliders to update function
    walk_range_slider.on_changed(update_sliders)
    stop_duration_slider.on_changed(update_sliders)
    pop_place_slider.on_changed(update_sliders)

    num_people = len(community.population)

    # initialize the scatter plot
    data = community.get_all_positions_x_y()
    x = data[:, 0]
    y = data[:, 1]
    c = np.full((num_people,), 0.5) # intialize color to green
    scat = ax.scatter(x, y, c=c, vmin=0, vmax=1,
                      cmap="jet", edgecolor="k")
    # plot popular places
    pop_places_x = [pos[0] for pos in community.popular_places]
    pop_places_y = [pos[1] for pos in community.popular_places]
    pop_scat = ax.scatter(pop_places_x,
                          pop_places_y,
                          marker="s",
                          alpha=0.5)

    # utility function to update key-value args with local variables
    def change_kwargs(orig_kwargs, **kwargs):
        orig_kwargs.update(kwargs)

    frame_count = 0
    total_frametime = 0
    def update(_):
        """Update the scatter plot."""
        nonlocal total_frametime, frame_count, data

        begin_time = time.perf_counter()

        # call the "before" function
        if before_callback:
            before_callback(*before_args, **before_kwargs)

        data = community.get_all_positions_x_y(nparray_to_fill=data)

        # Set x and y data (input in the form of a 2D np array)
        scat.set_offsets(data)

        # Set sizes of dots (we might not need this)
        # self.scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)

        # Set colors of dots
        # scat.set_array(c)

        # call the "after" function
        if after_callback:
            after_callback(*after_args, **after_args)

        total_time = time.perf_counter() - begin_time
        frametime = round(total_time*1000000, 2)
        total_frametime += frametime
        frame_count += 1
        if frame_count == 100:
            print("Average compute time in last {} frames: {:8.2f} microseconds".format(frame_count, total_frametime/frame_count))
            frame_count = 0
            total_frametime = 0

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return (scat,)

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
