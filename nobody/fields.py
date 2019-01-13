import numpy


class Field:
    """Base class for all Fields.
    
    Each field passed into a simulation contributes to the total force felt by each particle.
    As these fields are independent, the order in which they are considered does not affect
    particle behaviour.
    """

    def validate_setup(self, particles):
        """Raise any errors encountered with provided arguments."""
        pass

    def get_mask(self, particles):
        """Generate a boolean mask determining which particles to act upon."""
        raise NotImplementedError("Should be overridden in subclasses.")

    def update_acceleration(self, particles):
        """Update accelerations based on other particle parameters."""
        raise NotImplementedError("Should be overridden in subclasses.")


class FixedDirectionMixin:

    def validate_setup(self, particles):
        particle_dimensions = particles.dimensions
        if len(self.vector) != particle_dimensions:
            raise ValueError("A {}-dimensional vector should be provided."
                             .format(particle_dimensions))

    @staticmethod
    def normalise_vector(v):
        return v / numpy.linalg.norm(v)


class ConstantForce(Field, FixedDirectionMixin):
    """A constant field with a fixed magnitude and direction."""

    def __init__(self, vector, force):
        """Initialise field.

        Args:
            vector (tuple): A vector matching the dimensionality of the particles indicating the
                            direction of the force.
            force (float): The magnitude (in N) of the force to apply.
        """
        self.vector = self.normalise_vector(vector)
        self.force = force

    def acceleration_magnitude(self, particles):
        return self.force / particles.mass

    def get_mask(self, particles):
        return numpy.ones(particles.shape, bool)

    def update_acceleration(self, particles):
        mask = self.get_mask(particles)
        particles.a[mask] += self.vector * self.acceleration_magnitude


class ConstantAcceleration(ConstantForce):
    """An effective field providing a fixed acceleration to all particles."""

    def __init__(self, vector, acceleration):
        """Initialise field.

        Args:
            vector (tuple): A vector matching the dimensionality of the particles indicating the
                            direction of the acceleration.
            acceleration (float): The magnitude of the acceleration to apply.
        """
        self.vector = self.normalise_vector(vector)
        self.acceleration = acceleration

    def acceleration_magnitude(self, particles):
        return self.acceleration


class Wall(ConstantForce):
    """A hard wall.

    Particles are prevented from crossing the wall by an infinitely-strong force which acts
    if they cross the boundary.
    """

    def __init__(self, position, normal):
        """Initialise field.

        Args:
            position (tuple): A vector matching the dimensionality of the particles indicating the
                              position of the wall.
            normal (tuple): A vector matching the dimensionality of the particles indicating the
                            orientation of the wall.
        """
        self.position = position
        force = 999999999999  # A big number. Be smarter.
        super().__init__(vector=normal, force=force)

    def validate_setup(self, particles):
        particle_dimensions = particles.dimensions
        if len(self.position) != particle_dimensions:
            raise ValueError("A {}-dimensional position coordinate should be provided."
                             .format(particle_dimensions))
        super().validate_setup(particles)

    def get_mask(self, particles):
        plane_constant = numpy.dot(self.position, self.vector)
        return numpy.dot(particles.pos, self.vector) < plane_constant
