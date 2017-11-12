from fields import Field
from particles import Particles


class VelocityVerlet:
    """Calculate particle trajectories using the Velocity Verlet algorithm.

    An simple yet powerful algorithm which has seen use in a range of applications for many years.

    For more info, see:
    https://en.wikipedia.org/wiki/Verlet_integration#Velocity_Verlet
    """

    def __init__(self, particles, fields, timestep):
        """Initialise simulation.

        Args:
            particles (Particles): The particles to use.
            fields (list(Field)): A list of fields with which to update particle accelerations
                                  at each timestep.
            timestep (float): The amount of time (in seconds) that passes with each call to 'step'.
        """
        self.particles = particles
        self.timestep = timestep
        self.fields = fields
        self.validate_setup()

        self.t = 0

    def step(self):
        """Update particle positions and velocities."""
        dt = self.timestep

        # Calculate half-velocity using current acceleration and position
        v_half = self.particles.v + (0.5 * self.particles.a * dt)

        # Update position based on half-velocity
        self.particles.pos += v_half * dt

        # Calculate acceleration based on the combined action of active fields.
        self._update_acceleration()

        # Update velocity using calculated acceleration
        self.particles.v = v_half + (0.5 * self.particles.a * dt)

        self.t += dt

    def _update_acceleration(self):
        """Sum acceleration contributions of all active fields."""
        self.particles.a = 0
        for field in self.fields:
            field.update_acceleration()

    def validate_fields(self):
        fields = self.fields
        if type(fields) is not list:
            raise TypeError("Fields must be supplied as a list.")
        if not all(isinstance(field, Field) for field in fields):
            raise TypeError("Please supply valid 'Field' subclasses.")

    def validate_setup(self):
        if not type(self.particles, Particles):
            raise TypeError("Please supply a valid 'Particles' array.")
        self.validate_fields()
