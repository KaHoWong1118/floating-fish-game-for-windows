import random
import unittest
from aquarium import Aquarium


class AquariumTests(unittest.TestCase):
    def test_population_and_visitors_over_ten_minutes(self):
        world = Aquarium(900, 550, random.Random(4))
        seen, counts = set(), set()
        for _ in range(6000):
            world.update(.1)
            fish = [a for a in world.animals if not a.lifetime]
            visitors = [a for a in world.animals if a.lifetime]
            counts.add(len(fish))
            self.assertIn(len(fish), (1, 2))
            self.assertLessEqual(len(visitors), 1)
            seen.update(a.kind for a in visitors)
            for animal in world.animals:
                self.assertGreaterEqual(animal.x, 0)
                self.assertLessEqual(animal.x, 820)
        self.assertEqual(counts, {1, 2})
        self.assertEqual(seen, {'crab', 'shrimp'})

    def test_turn_at_edges(self):
        world = Aquarium(900, 550, random.Random(1))
        fish = world.animals[0]
        fish.x, fish.direction = 819, 1
        world.update(1)
        self.assertEqual((fish.x, fish.direction), (820, -1))
        fish.x, fish.direction = 1, -1
        world.update(1)
        self.assertEqual((fish.x, fish.direction), (0, 1))

    def test_visitor_expires(self):
        world = Aquarium(900, 550, random.Random(2))
        world.visitor_in = 0
        world.update(.1)
        visitor = next(a for a in world.animals if a.lifetime)
        world.update(18)
        self.assertNotIn(visitor, world.animals)

    def test_zero_time_does_not_move(self):
        world = Aquarium(900, 550, random.Random(3))
        before = [(a.x, a.y, a.age) for a in world.animals]
        world.update(0)
        self.assertEqual(before, [(a.x, a.y, a.age) for a in world.animals])


if __name__ == '__main__':
    unittest.main()
