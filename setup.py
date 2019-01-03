#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : setup.py
# @Desc    : ""


from setuptools import setup, find_packages
from alioth import (
    __version__ as version,
    __author__ as author,
    __author_email__ as author_email,
    __license__ as _license
)

setup(
    name='alioth',
    version=version,
    description="Alioth is an open-sourced remote vulnerability testing framework.",
    long_description="",
    classifiers=[],
    keywords='PoC,Exp,Alioth,Scanner',
    author=author,
    author_email=author_email,
    url='https://github.com/jeffzh3ng',
    license=_license,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'alioth = alioth.alioth_verify:main',
        ],
    },
)
