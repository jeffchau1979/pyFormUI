#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
	name = 'pyFormUI',
	version = '0.1',
	description = 'A Simple Form GUI for python',
	author = 'zhangfeng.zou',
	author_email = 'jeff.chau@hotmail.com',
	url = 'https://www.en7788.com',
	license="MIT",
    keywords = 'GUI wxpython Form',	
	package_dir = {
		'FormUI' : 'FormUI',
		'Demo' : 'Demo',
		'':'.'
	},
	packages=["Demo", "FormUI"],
	include_package_data=True,
	package_data = {
	   'Demo':['Demo/*.xml'],
	},
	install_requires=['wxpython'],
)
