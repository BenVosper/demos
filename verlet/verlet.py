import numpy


class VelocityVerlet:

    def __init__(self, data, potential, timestep):
        self.data = data
        self.potential = potential
        self.timestep = timestep

        self.t = 0

    def step(self):
        dt = self.timestep
        t_next = self.t + dt

        v_half = self.data["velocity"] + (0.5 * self.data["acceleration"] * dt)
        x_next = self.data["pos"] + (v_half * dt)

        a_next = self.potential(x_next)
        v_next = v_half + (0.5 * a_next * dt)

        self.data["pos"] = x_next
        self.data["velocity"] = v_next
        self.data["acceleration"] = a_next

        self.t = t_next
        
