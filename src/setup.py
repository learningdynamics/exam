from distutils.core import setup,Extension
from Cython.Build import cythonize
import numpy

## could not find the numpy path if using this
setup(
    ext_modules = cythonize("*.pyx"),
    include_dirs=[numpy.get_include()]
)

# setup(ext_modules = [ Extension("optimisation", ["optimisation.c"],
#                                include_dirs=[numpy.get_include()])
