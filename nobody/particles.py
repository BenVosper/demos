import numpy


class Particles(numpy.recarray):
    """Container for particle data.

    When called, provides an ~empty~ array of particles and associated parameters. Must be
    populated with meaningful data elsewhere.

    Numpy.recarray provides easy access to named columns as listed in 'Particles.dtype'.
    """

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
        dtype = [
            ("i", int),                            # Particle index
            ("mass", float),                       # Mass
            ("pos", float, dimensions),            # Position
            ("v", float, dimensions),              # Velocity
            ("a", float, dimensions),              # Acceleration
        ]
        dtype.extend(cls.extra_parameters)
        return super().__new__(cls, shape=n, dtype=dtype)

    @classmethod
    def validate_setup(cls):
        if cls.n < 1:
            raise ValueError("Number of particles must be positive and non-zero.")
        cls.validate_extra_parameters()

    @classmethod
    def validate_extra_parameters(cls):
        for name, dtype, *_ in cls.extra_parameters:
            if type(name) != str:
                raise TypeError("Extra parameter names must be strings.")
            if not isinstance(dtype, type) and not isinstance(dtype, numpy.dtype):
                raise TypeError("Invalid datatype provided for extra parameter.")
