import numpy


class Field:
    """Base class for all Fields.
    
    Each field passed into a simulation contributes to the total force felt by each particle.
    As these fields are independent, the order in which they are considered does not affect
    particle behaviour.
    """

    def __init__(self, particles, mask=None):
        """Initialise field.

        Args:
            particles (Particles): The particles to act upon
            mask (numpy.array (bool)): A boolean array with shape equal to the number of
                                       particles. Particles corresponding to False mask elements
                                       are not affected by the field. If not provided, all
                                       particles are affected.
        """
        self.particles = particles
        self.mask = mask or numpy.ones(self.particles.i.shape, bool)
        self.validate_setup()

    def validate_setup(self):
        """Raise any errors encountered with provided arguments."""
        pass

    def update_acceleration(self):
        """Update accelerations based on other particle parameters."""
        raise NotImplementedError("Should be overridden in subclasses.")


class FixedDirectionMixin:

    def validate_setup(self):
        particle_dimensions = self.particles.dimensions
        if len(self.vector) != particle_dimensions:
            raise ValueError("A {}-dimensional vector should be provided."
                             .format(particle_dimensions))

    @staticmethod
    def normalise_vector(v):
        return v / numpy.linalg.norm(v)


class ConstantForce(Field, FixedDirectionMixin):
    """A constant field with a fixed magnitude and direction."""

    def __init__(self, particles, vector, force, mask=None):
        """Initialise potential.

        Args:
            vector (tuple): A vector matching the dimensionality of the particles indicating the
                            direction of the force.
            force (float): The magnitude (in N) of the force to apply.
        """
        self.vector = self.normalise_vector(vector)
        self.force = force
        super().__init__(particles, mask)

    @property
    def acceleration_magnitude(self):
        return self.force / self.particles.mass

    def update_acceleration(self):
        self.particles.a[self.mask] += self.vector * self.acceleration_magnitude


class ConstantAcceleration(Field, FixedDirectionMixin):
    """An effective field providing a fixed acceleration to all particles."""

    def __init__(self, particles, vector, acceleration, mask=None):
        """Initialise potential.

        Args:
            vector (tuple): A vector matching the dimensionality of the particles indicating the
                            direction of the acceleration.
            acceleration (float): The magnitude of the acceleration to apply.
        """
        self.vector = self.normalise_vector(vector)
        self.acceleration = acceleration
        super().__init__(particles, mask)

    def update_acceleration(self):
        self.particles.a[self.mask] += self.vector * self.acceleration
