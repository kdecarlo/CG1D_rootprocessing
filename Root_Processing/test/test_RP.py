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
    
    def test_incorrect_input(self):
        '''assert error when processing option not listed in code is given'''
        analysis_list = ['RP_stitch']
        override = 1
        
        bad_analysis_list_sp = ['sitch']
        bad_analysis_list_str = 'RP_stitch'
        bad_analysis_list_int = 4
        
        bad_override_str = 'override'
        bad_override_int = 4
        
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_sp 1)
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_str, 1)
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_int, 1)
        
        self.assertRaises(ValueError, RP_run, wd, analysis_list, bad_override_str)
        self.assertRaises(ValueError, RP_run, wd, analysis_list, bad_override_int)

        
    '''Make a a non-functioning image'''
    '''Make an unreadable image'''
    '''
        