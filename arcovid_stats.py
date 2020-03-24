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

"""Add statistic functionalities to data tables

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
from datetime import datetime
import logging

import numpy as np

import pandas as pd

import diskcache as dcache


# =============================================================================
# CONSTANTS
# =============================================================================



# =============================================================================
# FUNCTIONS_
# =============================================================================


class TableStats(object):
    """
    Class to work with province - patient table as a function of time
    """

    def __init__(self, df):
        self.df = df

    @property
    def tot_casos_confirmados(self):
        """Returns latest value of total confirmed cases"""
        dates = [adate for adate in self.df.columns if isinstance(adate, datetime)]
        return self.df[('ARG', 'C'), dates[-1]] 

