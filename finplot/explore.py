# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/12/8 下午3:30
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

import datapane as dp
import pandas as pd
import polars as pl
import pygwalker as pyg
from IPython.display import display


def Table(table: pl.DataFrame | pd.DataFrame):
    """探索表格"""
    if isinstance(table, pl.DataFrame):
        table = table.to_pandas()
    return dp.DataTable(table)


def Chart(table: pl.DataFrame | pd.DataFrame):
    return pyg.walk(table)


def go(table: pl.DataFrame | pd.DataFrame):
    display(Table(table))
    display(Chart(table))
