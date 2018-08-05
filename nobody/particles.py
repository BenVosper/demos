import numpy

PARTICLES_DTYPE_2D = [
    ("i", int),                            # Particle index
    ("mass", float),                       # Mass
    ("pos", [                              # Position components:
        ("x", float),                      # - X
        ("y", float)]),                    # - Y
    ("v", [                                # Velocity components:
        ("x", float),                      # - X
        ("y", float)]),                    # - Y
    ("a", [                                # Acceleration components:
        ("x", float),                      # - X
        ("y", float)]),                    # - Y
]

PARTICLES_DTYPE_3D = [
    ("i", int),                            # Particle index
    ("mass", float),                       # Mass
    ("pos", [                              # Position components:
        ("x", float),                      # - X
        ("y", float),                      # - Y
        ("z", float)]),                    # - Z
    ("v", [                                # Velocity components:
        ("x", float),                      # - X
        ("y", float),                      # - Y
        ("z", float)]),                    # - Z
    ("a", [                                # Acceleration components:
        ("x", float),                      # - X
        ("y", float),                      # - Y
        ("z", float)]),                    # - Z
]


class Particles(numpy.recarray):
    """Container for particle data.

    When called, provides an ~empty~ array of particles and associated parameters. Must be
    populated with meaningful data elsewhere.

    Numpy.recarray provides easy access to named columns defined in 'PARTICLES_DTYPE's.
    """
    dtypes = {
        2: PARTICLES_DTYPE_2D,
        3: PARTICLES_DTYPE_3D
    }

    def __new__(cls, n, dimensions, extra_parameters=list()):
        """Initialise particles.

        Args:
            n (int): The number of particles. (Particles.shape will always return this)
            dimensions (int): The number of dimensions. For each vector parameter (position,
                              velocity acceleration, etc.) there will be this many individual
                              components.
            extra_parameters (list(tuple(str, type))): Any extra parameters to be added to the
                                                       array. List elements should be two-tuples
                                                       of parameter names and dtype to use.
        """
        cls.n = n
        cls.dimensions = dimensions
        cls.extra_parameters = extra_parameters
        cls.validate_setup()
        dtype = cls.dtypes[cls.dimensions]
        dtype.extend(cls.extra_parameters)
        return super().__new__(cls, shape=n, dtype=dtype)

    @classmethod
    def validate_setup(cls):
        if cls.n < 1:
            raise ValueError("Number of particles must be positive and non-zero.")
        if cls.dimensions not in [2, 3]:
            raise ValueError("Invalid number of dimensions. Try 2D or 3D.")
        cls.validate_extra_parameters()

    @classmethod
    def validate_extra_parameters(cls):
        for name, dtype in cls.extra_parameters:
            if type(name) != str:
                raise TypeError("Extra parameter names must be strings.")
            if not isinstance(dtype, type) and not isinstance(dtype, numpy.dtype):
                raise TypeError("Invalid datatype provided for extra parameter")


