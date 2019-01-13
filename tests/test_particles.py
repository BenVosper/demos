from unittest import TestCase

from nobody.particles import Particles


class TestParticles(TestCase):

    def test_particle_count_error(self):
        self.assertRaisesRegex(
            ValueError,
            "Number of particles must be positive and non-zero",
            Particles,
            0,
            dimensions=2
        )

    def test_extra_parameters(self):
        extra = [("foo", int)]
        particles = Particles(1, dimensions=2, extra_parameters=extra)
        self.assertEqual(particles.dtype.names[-1], "foo")
        self.assertEqual(particles.dtype[-1], int)

    def test_extra_parameters_name_error(self):
        self.assertRaisesRegex(
            TypeError,
            "Extra parameter names must be strings",
            Particles,
            1,
            dimensions=2,
            extra_parameters=[(b"not-a-string", float)]
        )

    def test_extra_parameters_type_error(self):
        self.assertRaisesRegex(
            TypeError,
            "Invalid datatype provided for extra parameter",
            Particles,
            1,
            dimensions=2,
            extra_parameters=[("foo", "not-a-type")]
        )
