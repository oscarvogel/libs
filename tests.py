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

import numpy as np

import pandas as pd

from matplotlib.testing.decorators import check_figures_equal

import arcovid19


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

LOCAL_CASES = PATH / "databases" / "cases.xlsx"


# =============================================================================
# SETUP
# =============================================================================

def setup_function(func):
    arcovid19.CACHE.clear()


# =============================================================================
# INTEGRATION
# =============================================================================

def test_load_cases_remote():
    local = arcovid19.load_cases(url=LOCAL_CASES)
    local = local[local.dates]
    local[local.isnull()] = 143

    remote = arcovid19.load_cases()
    remote = remote[remote.dates]
    remote[remote.isnull()] = 143

    assert np.all(local == remote)


# =============================================================================
# UNITEST
# =============================================================================

def test_load_cases_local():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df, arcovid19.CasesFrame)


def test_delegation():
    df = arcovid19.load_cases(url=LOCAL_CASES)

    assert repr(df) == repr(df.df)
    assert df.transpose == df.df.transpose


def test_dates():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df.dates, list)


def test_totcases():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df.tot_cases, float)


def test_last_grate():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df.last_growth_rate(), float)


def test_full_grate():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    assert isinstance(df.grate_full_period(), pd.Series)


def test_full_grate_provincias():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    for name, code in arcovid19.PROVINCIAS.items():
        wname = df.grate_full_period(provincia=name)
        wcode = df.grate_full_period(provincia=code)
        assert isinstance(wname, pd.Series)
        assert isinstance(wcode, pd.Series)


def test_grate_provincias():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    for name, code in arcovid19.PROVINCIAS.items():
        wname = df.last_growth_rate(provincia=name)
        wcode = df.last_growth_rate(provincia=code)

        if np.isnan(wname):
            assert np.isnan(wcode)
        else:
            assert wname == wcode


def test_grate_provincia_invalida():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    with pytest.raises(ValueError):
        df.last_growth_rate(provincia="colorado")


def test_get_item():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    value = df[df.provincia_status == f"CBA_C"]
    expected = df.df[df.provincia_status == f"CBA_C"]
    assert np.all(value == expected)


def test_restore_time_serie():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    tsdf = df.restore_time_serie()
    for prov in arcovid19.PROVINCIAS.values():
        for code in arcovid19.STATUS.values():
            orig_row = df.loc[(prov, code)][df.dates].values
            ts = tsdf.loc[(prov, code)][df.dates].values
            assert np.all(ts.cumsum() == orig_row)


# =============================================================================
# PLOTS
# =============================================================================

def test_invalid_plot_name():
    df = arcovid19.load_cases(url=LOCAL_CASES)
    with pytest.raises(ValueError):
        df.plot("_plot_df")


@check_figures_equal()
def test_plot_call(fig_test, fig_ref):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot(ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.grate_full_period_all(ax=exp_ax)


@check_figures_equal()
def test_plot_grate_full_period_all(fig_test, fig_ref):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("grate_full_period_all", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.grate_full_period_all(ax=exp_ax)


@check_figures_equal()
def test_plot_grate_full_period(fig_test, fig_ref):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("grate_full_period", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.grate_full_period(ax=exp_ax)


@check_figures_equal()
def test_plot_grate_full_period_all_equivalent_calls(fig_test, fig_ref):
    cases = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    fig_test.set_size_inches(12, 12)
    test_ax = fig_test.subplots()
    cases.plot.grate_full_period_all(ax=test_ax)
    test_ax.set_title("")

    # expected
    fig_ref.set_size_inches(12, 12)
    exp_ax = fig_ref.subplots()

    cases.plot.grate_full_period(
        deceased=False, active=False, recovered=False, ax=exp_ax)
    for prov in sorted(arcovid19.CODE_TO_POVINCIA):
        cases.plot.grate_full_period(
            prov, deceased=False, active=False, recovered=False, ax=exp_ax)

    exp_ax.set_title("")


@check_figures_equal()
def test_plot_time_serie_all(fig_test, fig_ref):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("time_serie_all", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.time_serie_all(ax=exp_ax)


@check_figures_equal()
def test_plot_time_serie(fig_test, fig_ref):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("time_serie", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.time_serie(ax=exp_ax)


@check_figures_equal()
def test_plot_time_serie_all_equivalent_calls(fig_test, fig_ref):
    cases = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    fig_test.set_size_inches(12, 12)
    test_ax = fig_test.subplots()
    cases.plot.time_serie_all(ax=test_ax)
    test_ax.set_title("")

    # expected
    fig_ref.set_size_inches(12, 12)
    exp_ax = fig_ref.subplots()

    cases.plot.time_serie(
        deceased=False, active=False, recovered=False, ax=exp_ax)
    for prov in sorted(arcovid19.CODE_TO_POVINCIA):
        cases.plot.time_serie(
            prov, deceased=False, active=False, recovered=False, ax=exp_ax)

    exp_ax.set_title("")


@check_figures_equal()
def test_plot_barplot(fig_test, fig_ref):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("barplot", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.barplot(ax=exp_ax)


@check_figures_equal()
def test_plot_boxplot(fig_test, fig_ref):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("boxplot", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.boxplot(ax=exp_ax)


# =============================================================================
# BUGS
# =============================================================================

@pytest.mark.parametrize(
    "plot_name", [
        "time_serie", "time_serie_all",
        "grate_full_period", "grate_full_period_all"])
def test_plot_all_dates_ticks(plot_name):
    df = arcovid19.load_cases(url=LOCAL_CASES)

    expected = [str(d.date()) for d in df.dates]

    ax = df.plot(plot_name)
    labels = [l.get_text() for l in ax.get_xticklabels()]
    ticks = ax.get_xticks()

    assert labels == expected
    assert len(labels) == len(ticks)
