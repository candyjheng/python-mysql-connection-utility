#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # pylint: disable=import-error

setup(
		name="mysql-connection-utility",
		author='candy.jheng',
		author_email='candy_love208@hotmail.com',
		version="0.0.1",
		description="MySQL database connection unitility",
		packages=find_packages(),
		install_requires=[
			"PyYAML >= 3.10, < 4.0",
			"mysqlclient >= 1.4.2, < 2.0.0",

		],
		classifiers=[
			"Development Status :: 5 - Production/Stable",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: 3.7",
		],
)
