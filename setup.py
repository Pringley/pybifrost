from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "pybifrost",
    version = "0.0.1",
    packages = find_packages(),

    author = "Ben Pringle",
    author_email = "ben.pringle@gmail.com",
    description = "A burning rainbow bridge between scripting languages",
    url = "http://github.com/Pringley/pybifrost",
    license = "Apache License (2.0)",
)
