from unittest import TestCase

from nobody.fields import Wall
from nobody.particles import Particles


class TestWall(TestCase):

    def test_mask_2d_simple(self):
        particles = Particles(1, dimensions=2)

        # Negative quadrants "walled off"
        wall = Wall(position=(0, 0), normal=(1, 0))

        # When X position is positive, wall will not act
        particles.pos = (1, 0)
        self.assertEqual(wall.get_mask(particles)[0], False)

        # But when it's negative, it will
        particles.pos = (-1, 0)
        self.assertEqual(wall.get_mask(particles)[0], True)

    def test_mask_2d(self):
        particles = Particles(4, dimensions=2)

        wall = Wall(position=(0, 0), normal=(1, 1))
        particles.pos = [
            (1, 1),            # Ahead of wall: should not be affected
            (3, -1),  # Ahead of wall in second quadrant: still unaffected
            (-2, -2),          # Wrong side of wall: should be affected
            (0, 0),            # On boundary: unaffected
        ]
        self.assertEqual(wall.get_mask(particles).tolist(), [
            False,
            False,
            True,
            False
        ])
