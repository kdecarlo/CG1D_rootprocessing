import numpy as np
from astropy.io import fits
import time
import scipy.ndimage as imp
import datetime

from scipy import ndimage
from skimage.morphology import skeletonize
import scipy.misc
from scipy.signal import medfilt
from PIL import Image
import os


def RP_userconfiganalysis(wd, analysis_pos, analysis):
    f = open(wd+'/user_config.txt', 'r')
    parameters = {}
    counter = 1
    for line in f:
        if (counter > analysis_pos[0]-1) & (counter < analysis_pos[1]+1):
            splitline = line.split(':')
            parameters_ = {splitline[0]:splitline[1].strip()}
            parameters = {**parameters, **parameters_}
        counter += 1
        
    #1. STITCH
    if analysis == 'RP_stitch':
        parameters['dimh_horzoffset'] = np.int(parameters['dimh_horzoffset'])
        parameters['dimh_vertoffset'] = np.int(parameters['dimh_vertoffset'])
        parameters['dimv_horzoffset'] = np.int(parameters['dimv_horzoffset'])
        parameters['dimv_vertoffset'] = np.int(parameters['dimv_vertoffset'])
        stitchval = parameters['stitch_order']
        stitchval = stitchval.split(',')
        counter = 0
        for val in stitchval:
            stitchval[counter] = np.int(val)
            counter += 1
        parameters['stitch_order'] = stitchval
    
    #2. CROP
    if analysis == 'RP_crop':
        cropmatval = parameters['cropmat']
        cropmatval = cropmatval.split(',')
        counter = 0
        for val in cropmatval:
            cropmatval[counter] = np.int(val)
            counter += 1
        parameters['cropmat'] = cropmatval
    
    #3. WC
    if analysis == 'RP_wc':
        parameters['b_w'] = np.float(parameters['b_w'])
        parameters['s_w'] = np.float(parameters['s_w'])
        parameters['s_a'] = np.float(parameters['s_a'])
        parameters['s_s'] = np.float(parameters['s_s'])
        parameters['x_s'] = np.float(parameters['x_s'])
        parameters['x_a'] = np.float(parameters['x_a'])
    
    #4. MASK
    if analysis == 'RP_mask':
        parameters['windowsize'] = np.int(parameters['windowsize'])
        parameters['threshold'] = np.float(parameters['threshold'])
        parameters['globthresh'] = np.float(parameters['globthresh'])
    
    #5. IMAGEFILTER
    if analysis == 'RP_imagefilter':
        parameters['bwareaval'] = np.int(parameters['bwareaval'])
        parameters['medfilterval'] = np.int(parameters['medfilterval'])
        
    #6. DISTMAP
    if analysis == 'RP_distmap':
        parameters['maxval'] = np.int(parameters['maxval'])
    
    #7. RADWC
    if analysis == 'RP_radwc':
        parameters['pixelbin'] = np.int(parameters['pixelbin'])
    
    #8. THICKNESS
    
    return(parameters)