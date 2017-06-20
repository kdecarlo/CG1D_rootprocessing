#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
	name = 'Root_Processing',
	version = '1.0.0', 
	author = 'Keita DeCarlo', 
	author_email = 'decarlokd@ornl.gov', 
	packages = find_packages(exclude=['tests, 'notebooks']),
	include_package_data = True, 
	test_suite = 'tests', 
	install_requires = [
		'numpy', 
		'astropy',
		'time',
		'scipy',
		'datetime',
		'skimage',
		'PIL',
		'os',
		'sys',
		],
		dependency_links = [
		],
		description = 'Root Processing suite for images at the ORNL CG-1D beamline',
		license = 'BSD',
		'keywords = 'tiff tif root processing',
		url = 'https://github.com/kdecarlo/CG1D_rootprocessing',
		classifiers = ['Development Status :: 1 - Alpha', 
						'Topic :: Scientific/Engineering :: Biological Sciences',
						'Intended Audience :: General User Population',
						'Programming Language :: Python :: 2.7',
						'Programming Language :: Python :: 3.5'],
)