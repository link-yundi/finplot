# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/12/8 下午3:30
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

import pandas as pd
import polars as pl
import pygwalker as pyg
from IPython.display import display


def Chart(table: pl.DataFrame | pd.DataFrame):
    return pyg.walk(table)


def go(table: pl.DataFrame | pd.DataFrame):
    display(Chart(table))
