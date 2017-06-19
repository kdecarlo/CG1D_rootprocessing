import unittest
import unittest
import numpy as np
import os
from PIL import Image

import sys
#sys.path.append(wd+'/Analyses')
#sys.path.append(wd+'/Misc')

class TestClass(unittest.TestCase):
    
    def setup(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../'))
        
    
    def test_incorrect_input(self):
                                         
                                         
        '''assert error when processing option not listed in code is given'''
        analysis_list = ['RP_stitch']
        override = 1
        
        bad_analysis_list_sp = ['sitch']
        bad_analysis_list_str = 'RP_stitch'
        bad_analysis_list_int = 4
        
        bad_override_str = 'override'
        bad_override_int = 4
                                         
        wd = self.data_path
        #sys.path.append(wd+'/Analyses')    Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
                                                                                  
        from RP_run import RP_run                                  
        
        #With override option
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_sp, 1)
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_str, 1)
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_int, 1)
        
        #Without override option
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_sp, 0)
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_str, 0)
        self.assertRaises(ValueError, RP_run, wd, bad_analysis_list_int, 0)
        
        self.assertRaises(ValueError, RP_run, wd, analysis_list, bad_override_str)
        self.assertRaises(ValueError, RP_run, wd, analysis_list, bad_override_int)                                         

    def test_stitch(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run                                  

        sampledata(wd, 1)
        analysis_list = ['RP_stitch']
        
        #user_config-specified image/actual image mismatch - due to number, incorrect file format, etc.
        os.remove(wd+'/Sample_Data_unittest/19000101_Image_0060_0006.tiff')
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        #image sizes are not consistent
        bad_image = np.zeros([100, 100])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/19000101_Image_0060_0006.tiff')
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1) 
        
        shutil.rmtree(wd+'/Sample_Data_unittest') 
    
    def test_crop(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run  
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/stitched')
        analysis_list = ['RP_crop']
        
        #Stitched image not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        #Cropmat values are greater/larger than the inputted image
        bad_image = zeros([20, 20])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/stitched/SampleImg_stitched.tiff')
        
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        shutil.rmtree(wd+'/Sample_Data_unittest') 

        
    def test_wc(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/crop')
        analysis_list = ['RP_wc']
        
        #Cropped image not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
                
        shutil.rmtree(wd+'/Sample_Data_unittest') 

    def test_mask(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/crop')
        analysis_list = ['RP_mask']
        
        #Cropped image not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        #Image is too small - windowsize is larger than image
        bad_image = zeros([5, 5])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/crop/SampleImg_crop.tiff')
        
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        shutil.rmtree(wd+'/Sample_Data_unittest') 
    
    def test_imagefilter(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask')
        analysis_list = ['RP_imagefilter']
        
        #mask image not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
    def test_distmap(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask_filter')
        analysis_list = ['RP_distmap']
        
        #mask image not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        #Mask image has no object to analyze
        bad_image = zeros([5, 5])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/mask_filter/SampleImg_filter.tiff')
        
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)

    def test_radwc(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/wc')
        os.makedirs(wd+'/Sample_Data_unittest/distmap')
        os.makedirs(wd+'/Sample_Data_unittest/mask')
        analysis_list = ['RP_radwc']
        
        #wc, distmap, mask images not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        
    
    def test_thickness(self):
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask_filter')
        analysis_list = ['RP_thickness']
        
        #mask image not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
    
    def test_rootimage(self):
        
        wd = self.data_path
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask_filter')
        os.makedirs(wd+'/Sample_Data_unittest/wc')
        analysis_list = ['RP_rootimage']
        
        #wc, mask images not found
        self.assertRaises(ValueError, RP_run, wd, analysis_list, 1)
        
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        