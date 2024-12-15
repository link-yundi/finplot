# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/11/5 下午5:32
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

from setuptools import setup, find_packages
import os

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), encoding="utf-8") as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

VERSION = get_version("finplot/__init__.py")

setup(
    name='finplot',
    version=VERSION,
    install_requires=['pandas',
                      'matplotlib',
                      'pyecharts',
                      'plotly',
                      'polars',
                      'ipywidgets',
                      'datapane',
                      'jupyterlab',
                      'jupyterlab-vim',
                      'jupyterlab_execute_time',
                      'JLDracula',
                      'jupyterlab-lsp',
                      'python-lsp-server[all]',
                      'pygwalker'],

    author='ZhangYundi',
    author_email='yundi.xxii@outlook.com',
    packages=find_packages(include=['finplot', 'finplot.*',]),
    description='Finance Plot',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/link-yundi/finplot.git',

    scripts=[],
    package_data={},
)
