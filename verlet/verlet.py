from potentials import Potential


class VelocityVerlet:

    def __init__(self, data, potential, timestep):
        self.data = data
        self.timestep = timestep

        if not type(potential) == list:
            self.potential = [potential]
        else:
            self.potential = potential
        self.validate_potentials(self.potential)

        self.t = 0

    def step(self):
        dt = self.timestep
        t_next = self.t + dt

        vx_half = self.data.v.x + (0.5 * self.data.a.x * dt)
        vy_half = self.data.v.y + (0.5 * self.data.a.y * dt)

        self.data.x += (vx_half * dt)
        self.data.y += (vy_half * dt)

        self._update_acceleration()

        self.data.v.x = vx_half + (0.5 * self.data.a.x * dt)
        self.data.v.y = vy_half + (0.5 * self.data.a.y * dt)

        self.t = t_next

    def _update_acceleration(self):
        self.data.a = 0
        for potential in self.potential:
            potential.update_acceleration()

    @staticmethod
    def validate_potentials(potentials):
        for potential in potentials:
            assert isinstance(potential, Potential)
