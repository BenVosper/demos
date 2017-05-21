import numpy

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.events import Pan, PanEnd

n = 10
xr = 100
yr = 100

p = figure(x_range=(0, xr), y_range=(0, yr), toolbar_location=None)
p.toolbar.active_drag = None

x_init = numpy.random.randint(0, xr, size=n)
y_init = numpy.random.randint(0, yr, size=n)

r, g, b = (numpy.random.randint(0, 255, size=n),
           numpy.random.randint(0, 255, size=n),
           numpy.random.randint(0, 255, size=n))
hexs = numpy.array(["#%02x%02x%02x" % (r, g, b) for r, g, b in zip(r, g, b)])

radii = (numpy.random.random(size=n) * 5) + 1

source = ColumnDataSource({'x': x_init,
                           'y': y_init,
                           'radius': radii,
                           'color': hexs,
                           'alpha': numpy.full(n, 0.6)})
circles = p.circle(x="x", y="y", radius="radius", color="color", fill_alpha="alpha", source=source)


def update(source_dict=source):
    """Random walk for input glyphs."""
    data = source_dict.data.copy()
    y = data["y"]
    x = data["x"]

    x_move = numpy.random.randint(-1, 2, size=n)
    y_move = numpy.random.randint(-1, 2, size=n)

    y += y_move
    x += x_move

    y = numpy.clip(y, 0, yr)
    x = numpy.clip(x, 0, xr)

    data["y"] = y
    data["x"] = x

    source_dict.data = data


def over_point(point_x, point_y, x, y, radii):
    """Return the indices of glyphs within a given distance of input coordinates."""

    dist_x = (x - point_x) ** 2
    dist_y = (y - point_y) ** 2

    over = (dist_x + dist_y) < 40

    return numpy.where(over)[0]


def move(event):
    source_data = source.data

    point_indices = over_point(event.x, event.y, source_data["x"], source_data["y"], source_data["radius"])

    if point_indices.size > 0:
        to_patch = {"x": [(index, event.x) for index in point_indices],
                    "y": [(index, event.y) for index in point_indices],
                    "alpha": [(index, 0.9) for index in point_indices]}

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
doc.add_periodic_callback(update, 16)
