from __future__ import print_function
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

import sys
import numpy
try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

# We need to find PySPICE. Can be done in one of two ways:
# Set the environment variable $PYSPICE, or use
# --with-pyspice=/direcory/to/pyspice
argv_replace = []
for arg in sys.argv:
    argv_replace.append(arg)
sys.argv = argv_replace

# The following is the command to use for building in-place for development
# python setup.py build_ext --inplace

cmdclass = {}
ext_modules = []

if use_cython:
    print("Using cython...")
    src = ["pint/cutils/str2ld_py.pyx"]
else:
    print("Using existing 'C' source file...")
    src = ["pint/cutils/str2ld_py.c"]

ext_modules += [Extension("pint.str2ld", src,
                          include_dirs = [numpy.get_include(),],
                          )]

if use_cython:
    cmdclass.update({'build_ext': build_ext})


import versioneer
cmdclass.update(versioneer.get_cmdclass())

# These command-line scripts will be built by the setup process and installed in your PATH
# See http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point
console_scripts = [ 'nicerphase=pint.scripts.nicerphase:main',
                    'event_optimize=pint.scripts.event_optimize:main',
                    'pintempo=pint.scripts.pintempo:main', 
                    'zima=pint.scripts.zima:main', 
                    'pintbary=pint.scripts.pintbary:main', 
                    'fermiphase=pint.scripts.fermiphase:main' ]

setup(
    name="pint",
    version = versioneer.get_version(),
    description = 'A Pulsar Timing Package, written in Python from scratch',

    author = 'Luo Jing, Scott Ransom, Paul Demorest, Paul Ray, et al.',
    author_email = 'sransom@nrao.edu',
    url = 'https://github.com/nanograv/PINT',
    license = 'TBD',

    install_requires = ['astropy>=1.2'],

    entry_points={  
        'console_scripts': console_scripts, 
    },

    packages=['pint',
        'pint.extern',
        'pint.models',
        'pint.models.stand_alone_psr_binaries',
        'pint.observatory',
        'pint.orbital'],

    package_data={
        'pint': ['datafiles/*']
    },
    cmdclass = cmdclass,
    ext_modules=ext_modules,
    #test_suite='tests',
    #tests_require=[]
)
