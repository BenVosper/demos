import numpy

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.events import Pan, PanEnd

from potentials import Well2D
from verlet import VelocityVerlet

fps = 60
frametime = 1000 / fps

n = 10
xr = 100
yr = 100

data = numpy.zeros(n, dtype=[("x", float),
                             ("y", float),
                             ("mass", float),
                             ("v", [("x", float), ("y", float)]),
                             ("a", [("x", float), ("y", float)]),
                             ])


data["x"] = numpy.random.random(n) * xr
data["y"] = numpy.random.random(n) * yr

data["mass"] = 1

wellxy = (50, 50)

well = Well2D(2, (wellxy[0], wellxy[1]), data)
verlet = VelocityVerlet(data, well, 0.1)

r, g, b = (numpy.random.randint(0, 255, size=n),
           numpy.random.randint(0, 255, size=n),
           numpy.random.randint(0, 255, size=n))
hexs = numpy.array(["#%02x%02x%02x" % (r, g, b) for r, g, b in zip(r, g, b)])

source = ColumnDataSource({'x': data["x"],
                           'y': data["y"],
                           'color': hexs,
                           'alpha': numpy.full(n, 0.6)})

p = figure(x_range=(0, xr), y_range=(0, yr), toolbar_location=None)
p.toolbar.active_drag = None

p.circle(x="x", y="y", radius=10, color="color", fill_alpha="alpha", source=source)
p.circle(x=wellxy[0], y=wellxy[1], radius=3, color="red")


def update(source_dict=source):
    d = source_dict.data
    verlet.step()
    d["x"] = verlet.data["x"]
    d["y"] = verlet.data["y"]
    source_dict.data = d


def over_point(point_x, point_y, x, y):
    """Return the indices of glyphs within a given distance of input coordinates."""

    dist_x = (x - point_x) ** 2
    dist_y = (y - point_y) ** 2

    over = (dist_x + dist_y) < 40

    return numpy.where(over)[0]


def move(event):
    source_data = source.data

    point_indices = over_point(event.x, event.y, source_data["x"], source_data["y"])

    if point_indices.size > 0:
        to_patch = {"x": [(index, event.x) for index in point_indices],
                    "y": [(index, event.y) for index in point_indices],
                    "alpha": [(index, 0.9) for index in point_indices]}

        for index in point_indices:
            data["v"]["x"][index] = 0
            data["v"]["y"][index] = 0

        source.patch(to_patch)


def restore_alpha(event):
    source_dict = source.data.copy()

    # Shouldn't have to re-construct this array here, but I can't get it to work with a copy()
    source_dict["alpha"] = numpy.full(n, 0.6)
    source.data = source_dict

p.on_event(Pan, move)
p.on_event(PanEnd, restore_alpha)

doc = curdoc()
doc.add_root(p)
doc.add_periodic_callback(update, frametime)
