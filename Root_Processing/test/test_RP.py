import unittest
import unittest
import numpy as np
import os
from PIL import Image

import sys
wd = '/Users/kdecarlo/Python_scripts/Root_Processing'
sys.path.append(wd+'/Analyses')
sys.path.append(wd+'/Misc')
from RP_run import RP_run

class TestClass(unittest.TestCase):
    '''Ask Jean for details here'''
    '''
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../notebooks/data_2_circles.tif'))
        
    def test_default_initialization(self):
        
        """assert if all parameters are coorectly set up when no parameters passed in"""
        o_calculate = CalculateRadialProfile()
        assert o_calculate.data == []
        assert o_calculate.center == {}
        assert o_calculate.angle_range == {}
        
    def test_initialization(self):
        my_data = np.array([1,2,3])
        my_center = {'x0': 0.5,
                     'y0': 1.1}
        my_angle_range = {'from': 0,
                          'to': 90}
        o_calculate = CalculateRadialProfile(data=my_data,
                                             center=my_center,
                                             angle_range=my_angle_range)
        assert (o_calculate.data == my_data).all()
        assert o_calculate.center == my_center
assert o_calculate.angle_range == my_angle_range
    '''
    
    def test_incorrect_input(self):
        '''assert error when processing option not listed in code is given'''
        bad_analysis_list = ['sitch']
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list, 1)
        