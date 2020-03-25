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

import os
import pathlib

import pytest

import arcovid19


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

LOCAL_CASES = PATH / "databases" / "cases.xlsx"


# =============================================================================
# TESTS
# =============================================================================

def setup_function(func):
    arcovid19.CACHE.clear()


def test_load_cases_local():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df, arcovid19.CasesFrame)


def test_load_cases_remote():
    df = arcovid19.load_cases()
    assert isinstance(df, arcovid19.CasesFrame)


def test_delegation():
    df = arcovid19.load_cases(url=LOCAL_CASES)

    assert repr(df) == repr(df.df)
    assert df.transpose == df.df.transpose


def test_dates():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df.dates, tuple)


def test_totcases():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df.tot_cases, float)


def test_r0():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df.r0(), float)


def test_r0_provincias():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    for name, code in arcovid19.PROVINCIAS.items():
        assert df.r0(provincia=name) == df.r0(provincia=code)


def test_r0_provincia_invalida():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    with pytest.raises(ValueError):
        df.r0(provincia="colorado")
