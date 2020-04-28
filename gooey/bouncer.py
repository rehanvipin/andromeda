from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

import random


NUMBER_OF_PEOPLE = 30
WALKING_SPEED = 100.0
SIMULATION_SPEED = 1.0/120.0
PERSON_SIZE = 50

class Fellow(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    colz = ListProperty([0., 1., 0.])
    sober = True

    def walk(self, dt):
        self.pos = Vector(*self.velocity)*dt + self.pos


class LocalBar(Widget):
    patrons = []
    cases = StringProperty()

    def populate(self):
        x,y = Window.size       # HACK, need to fix
        for _ in range(NUMBER_OF_PEOPLE):
            newbie = Fellow()
            newbie.center = (random.randint(0,x), random.randint(0,y))
            velocity = Vector(random.random()+1, random.random()+1)
            newbie.velocity = velocity.rotate(random.randint(0,360))
            # randomly insert drunk people
            if random.random() > 0.8:
                newbie.sober = False
                newbie.colz = [1,0,0]
            self.patrons.append(newbie)
            self.add_widget(newbie)
        self.cases = str(sum([not patron.sober for patron in self.patrons]))
    
    def update(self, dt):
        if int(self.cases == NUMBER_OF_PEOPLE):
            return
        for patron in self.patrons:
            patron.walk(1)
            if (patron.y < 0) or (patron.top > self.height):
                patron.velocity_y *= -1
            elif (patron.x < 0) or (patron.right > self.width):
                patron.velocity_x *= -1
            if patron.sober:
                continue

            # Pass on the drinks, with 80% probability, some people seem immune XD
            for otherpatron in (person for person in self.patrons if person.sober):
                if patron is otherpatron:
                    continue
                distance = ((patron.center_x - otherpatron.center_x)**2 + (patron.center_y - otherpatron.center_y)**2)
                if distance < PERSON_SIZE:
                    if random.random() < 0.8:
                        otherpatron.sober = False
                        otherpatron.colz = [1,0,0]
    
        self.cases = str(sum([not patron.sober for patron in self.patrons]))

    def on_touch_down(self, touch):
        print(touch)
    

class BouncerApp(App):
    def build(self):
        TheBar = LocalBar()
        TheBar.populate()
        Clock.schedule_interval(TheBar.update, SIMULATION_SPEED)
        return TheBar


if __name__ == "__main__":
    BouncerApp().run()