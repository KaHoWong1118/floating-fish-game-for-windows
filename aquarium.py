"""Desktop animal simulation, independent of the graphical interface."""
from dataclasses import dataclass
import math
import random


@dataclass
class Animal:
    kind: str
    x: float
    y: float
    speed: float
    direction: int
    phase: float
    age: float = 0.0
    lifetime: float = 0.0


class Aquarium:
    def __init__(self, width, height, rng=None):
        self.width, self.height = width, height
        self.rng = rng or random.Random()
        self.animals = [self._fish() for _ in range(self.rng.randint(1, 2))]
        self.visitor_in = self.rng.uniform(8, 15)
        self.fish_change_in = self.rng.uniform(20, 35)
        self.elapsed = 0.0

    def _fish(self):
        return Animal(self.rng.choice(('goldfish', 'bluefish', 'pinkfish')),
                      self.rng.uniform(0, max(0, self.width - 120)),
                      self.rng.uniform(self.height * .15, self.height * .65),
                      self.rng.uniform(25, 55), self.rng.choice((-1, 1)),
                      self.rng.uniform(0, math.tau))

    def update(self, dt, sprite_width=80):
        if dt < 0:
            raise ValueError('Time step must be nonnegative')
        self.elapsed += dt
        right = max(0, self.width - sprite_width)
        for animal in self.animals:
            animal.age += dt
            animal.x += animal.speed * animal.direction * dt
            if animal.x >= right:
                animal.x, animal.direction = right, -1
            elif animal.x <= 0:
                animal.x, animal.direction = 0, 1
        self.animals = [a for a in self.animals if not a.lifetime or a.age < a.lifetime]
        self.fish_change_in -= dt
        if self.fish_change_in <= 0:
            fish = [a for a in self.animals if not a.lifetime]
            if len(fish) == 2:
                self.animals.remove(fish[0])
            else:
                self.animals.append(self._fish())
            self.fish_change_in = self.rng.uniform(20, 35)
        self.visitor_in -= dt
        if self.visitor_in <= 0 and not any(a.lifetime for a in self.animals):
            self.animals.append(Animal(self.rng.choice(('crab', 'shrimp')), right / 2,
                                       max(0, self.height - 110), self.rng.uniform(15, 30),
                                       self.rng.choice((-1, 1)), 0, lifetime=18))
            self.visitor_in = self.rng.uniform(35, 60)

    def position(self, animal):
        amplitude = 2 if animal.kind == 'crab' else 8
        return animal.x, animal.y + math.sin(self.elapsed * 1.8 + animal.phase) * amplitude
