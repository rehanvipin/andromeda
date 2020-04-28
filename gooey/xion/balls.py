#!/usr/bin/env python
"""
Bouncing balls
"""
from random import random

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget


DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100.0


class Ball(Widget):
    """Class for bouncing ball."""
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def update(self, dt):
        self.pos = Vector(*self.velocity) * dt + self.pos


class BallsContainer(Widget):
    """Class for balls container, a main widget."""

    def update(self, dt):
        balls = (c for c in self.children if isinstance(c, Ball))
        for ball in balls:
            ball.update(dt)

            # bounce of walls
            # (note: Y axis is pointing *up*)
            if ball.x < 0 or ball.right > self.width:
                ball.velocity_x *= -1
            if ball.y < 0 or ball.top > self.height:
                ball.velocity_y *= -1

    def on_touch_up(self, touch):
        """Touch (or click) 'up' event: releasing the mouse button
        or lifting finger.
        """
        for _ in range(1):
            ball = Ball()
            ball.center = (touch.x, touch.y)
            ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),
                            -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
            self.add_widget(ball)


class BallsApp(App):
    """Represents the whole application."""

    def build(self):
        """Entry point for creating app's UI."""
        root = BallsContainer()
        Clock.schedule_interval(root.update, DELTA_TIME)
        return root


if __name__ == '__main__':
    BallsApp().run()