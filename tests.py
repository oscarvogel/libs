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

"""Test suite

"""


# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd

import pytest

import arcovid19


# =============================================================================
# TESTS
# =============================================================================


def test_load_cases():

    assert isinstance(arcovid19.load_cases(), pd.DataFrame)
    assert isinstance(arcovid19.load_cases(orientation="wide"), pd.DataFrame)

    with pytest.raises(ValueError):
        arcovid19.load_cases(orientation="foo")
