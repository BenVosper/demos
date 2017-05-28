import numpy


class Potential:

    def __init__(self, data, mask=None):
        self.data = data
        if mask is not None:
            self.mask = mask
        else:
            self.mask = numpy.ones(self.data.shape[0], bool)


class Well2D(Potential):

    def __init__(self, depth, pos, data, mask=None):
        self.depth = depth
        self.well_x, self.well_y = pos
        super().__init__(data, mask)

    def f(self):
        x = self.data.x
        y = self.data.y

        dx = x - self.well_x
        dy = y - self.well_y

        mdx = dx / self.well_x
        mdy = dy / self.well_y

        fx = -1 * numpy.sign(dx) * (mdx ** self.depth)
        fy = -1 * numpy.sign(dy) * (mdy ** self.depth)

        return fx, fy

    def update_acceleration(self):
        fx, fy = self.f()

        self.data.a.x[self.mask] += (fx / self.data.mass)[self.mask]
        self.data.a.y[self.mask] += (fy / self.data.mass)[self.mask]
