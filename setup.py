#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Mauricio Koraj, Vanessa Daza,
#                     Juan B Cabral, Mariano Dominguez, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""This file is for distribute pert

"""


# =============================================================================
# IMPORTS
# =============================================================================

import pathlib
import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages  # noqa


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

REQUIREMENTS = [
    "numpy", "pandas", "clize", "diskcache",
    "xlrd", "attrs",
    "matplotlib", "seaborn"]


with open(PATH / "README.rst") as fp:
    LONG_DESCRIPTION = fp.read()


DESCRIPTION = (
    "Utilities to access different Argentina-Related databases of "
    "COVID-19 data from the IATE task force.")


with open(PATH / "arcovid19.py") as fp:
    VERSION = [
        l for l in fp.readlines() if l.startswith("__version__")
    ][0].split("=", 1)[-1].strip().replace('"', "")


# =============================================================================
# FUNCTIONS
# =============================================================================

def do_setup():
    setup(
        name="arcovid19",
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author="IATE COVID-19 Task Force",
        author_email="jbc.develop@gmail.com",
        url="https://github.com/ivco19/libs",
        license="BSD-3",
        keywords=["covid-19", "project", "datasets", "argentina"],
        classifiers=(
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering"),
        py_modules=["arcovid19", "ez_setup"],
        entry_points={
            'console_scripts': ['arcovid19=arcovid19:main']},
        install_requires=REQUIREMENTS)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    do_setup()
