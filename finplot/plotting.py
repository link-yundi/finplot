# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/12/9 下午1:29
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Boxplot
from pyecharts.globals import CurrentConfig, NotebookType

from .options import Options

CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB


def table(tb_data: pd.DataFrame, highlight_cols: list[str] = None):
    """绘制表格"""
    cols = tb_data.columns
    cellvalues = [[f'<b>{val}</b>' for val in tb_data[cols[0]]]]
    if highlight_cols is not None:
        col_dict = {k: 1 for k in highlight_cols}
        for col in cols[1:]:
            if col in col_dict:
                cellvalues.append([f'<b>{val}</b>' for val in tb_data[col].tolist()])
            else:
                cellvalues.append(tb_data[col])
    else:
        for col in cols[1:]:
            cellvalues.append(tb_data[col].tolist())
    tb = go.Table(
        header=dict(
            values=[f"<b>{col}</b>" for col in tb_data.columns],
            **Options.Table.header,
        ),
        cells=dict(
            values=cellvalues,  # [d.tolist() for g, d in tb_data.items()],
            **Options.Table.cell,
            fill=dict(color=['gold', 'white']),
        )
    )
    return go.Figure(data=[tb])


def distplot(data: pd.Series | pd.DataFrame, bin_size):
    """分布图: 每一列都是一组数据集"""
    if isinstance(data, pd.Series):
        data = data.to_frame()
    hist_data = list()
    group_labels = list()
    for col_name, col_data in data.items():
        hist_data.append(col_data.dropna())
        group_labels.append(col_name)
    fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size, colors=Options.colors)
    fig.update_layout(**Options.layout, )
    if data.index.name == "date":
        fig.update_xaxes(hoverformat='%Y-%m-%d', tickformat="%Y-%m-%d")
    return fig


def bar(data: pd.Series | pd.DataFrame, title: str = None):
    """index是x-axis, columns是datasets"""
    if isinstance(data, pd.Series):
        data = data.to_frame()
    x_axis = data.index.tolist()
    cols = data.columns
    bar = (
        Bar(init_opts=opts.InitOpts(width="100%"))
        .add_xaxis(x_axis)
        .set_global_opts(**Options.get_echarts_options(title=title))
    )
    length = len(Options.colors)
    for i, name in enumerate(cols):
        dataset = data[name].tolist()
        bar.add_yaxis(
            name,
            dataset,
            color=Options.colors[i % length],
            label_opts=opts.LabelOpts(is_show=False)
        )
    return bar


def box(data: pd.Series | pd.DataFrame, title: str = None):
    """箱图, 每一列是一个dataset"""
    if isinstance(data, pd.Series):
        data = data.to_frame()
    x_axis = data.index.unique().dropna().tolist()
    x_axis.sort()
    chart = (
        Boxplot(init_opts=opts.InitOpts(width="100%"))
        .add_xaxis(x_axis, )
        .set_global_opts(**Options.get_echarts_options(title=title))
    )
    chart_data_all = dict()
    for name, dataset in data.items():
        chart_data = list()
        for i in x_axis:
            y = dataset[i]
            chart_data.append(y.dropna().tolist())
        chart_data_all[name] = chart.prepare_data(chart_data)
    for i, dataset_name in enumerate(data.columns):
        border_color = Options.colors[i % len(Options.colors)]
        fill_color = Options.get_colors(0.5)[i % len(Options.colors)]
        chart_data = chart_data_all[dataset_name]
        chart.add_yaxis(
            dataset_name,
            chart_data,
            itemstyle_opts=opts.ItemStyleOpts(
                border_color=border_color,  # 边框颜色
                border_width=2,  # 边框宽度
                color=fill_color,  # 箱体填充颜色
            )
        )

    return chart


def lines(data: pd.Series | pd.DataFrame, title: str = None):
    """曲线图 index是x-axis, columns是datasets"""
    if isinstance(data, pd.Series):
        data = data.to_frame()
    x_axis = data.index.tolist()
    cols = data.columns
    line = (
        Line(init_opts=opts.InitOpts(width="100%"))
        .add_xaxis(x_axis, )
        .set_global_opts(**Options.get_echarts_options(title=title))
    )
    length = len(Options.colors)
    for i, name in enumerate(cols):
        dataset = data[name].tolist()
        line.add_yaxis(
            name,
            dataset,
            is_symbol_show=False,
            color=Options.colors[i % length],
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
    return line


def violin(data: pd.Series | pd.DataFrame):
    """index是x-axis, columns是datasets"""
    if isinstance(data, pd.Series):
        data = data.to_frame()
    fig = go.Figure()
    x_axis = data.index
    cols = data.columns
    for i, name in enumerate(cols):
        dataset = data[name]
        fig.add_trace(
            go.Violin(
                x=x_axis,
                y=dataset,
                name=name,
                marker_color=Options.colors[i % len(Options.colors)],
                box_visible=True,
                meanline_visible=True,
            )
        )

    fig.update_layout(**Options.layout, )
    if data.index.name == "date":
        fig.update_xaxes(hoverformat='%Y-%m-%d', tickformat="%Y-%m-%d")
    return fig
