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


def userconfiganalysis(wd, analysis_pos, analysis):
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
    if analysis == 'stitch':
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
    
    return(parameters)