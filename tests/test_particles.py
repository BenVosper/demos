from unittest import TestCase

from nobody.particles import Particles, PARTICLES_DTYPE_2D, PARTICLES_DTYPE_3D


class TestParticles(TestCase):

    def test_dtype_2d(self):
        particles = Particles(1, dimensions=2)
        self.assertTrue(particles.dtype, PARTICLES_DTYPE_2D)
        for attr, attr_type in PARTICLES_DTYPE_2D:
            self.assertTrue(hasattr(particles, attr))
            if isinstance(attr_type, list):
                for sub_attr, _ in attr_type:
                    self.assertTrue(hasattr(getattr(particles, attr), sub_attr))

    def test_dtype_3d(self):
        particles = Particles(1, dimensions=3)
        self.assertTrue(particles.dtype, PARTICLES_DTYPE_3D)
        for attr, attr_type in PARTICLES_DTYPE_3D:
            self.assertTrue(hasattr(particles, attr))
            if isinstance(attr_type, list):
                for sub_attr, _ in attr_type:
                    self.assertTrue(hasattr(getattr(particles, attr), sub_attr))

    def test_dtype_error(self):
        self.assertRaisesRegex(
            ValueError,
            "Invalid number of dimensions",
            Particles,
            1,
            dimensions=4
        )

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
        expected_dtype = PARTICLES_DTYPE_2D.copy()
        expected_dtype.extend(extra)
        particles = Particles(1, dimensions=2, extra_parameters=extra)
        self.assertEqual(particles.dtype, expected_dtype)
        self.assertTrue(hasattr(particles, "foo"))

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
