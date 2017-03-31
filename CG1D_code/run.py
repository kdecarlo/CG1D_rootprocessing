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

from IOfilecheck import IOfilecheck
from timer import timer
from stitch import stitch
from userconfiganalysis import userconfiganalysis

def run(wd, analysis_list, override = 0):
    
    #User config analysis positions:
    #1. Stitch
    analysis_pos_list = {
        'stitch':[2, 10]
    }
    
    
    
    #Dispatch
    dispatch = {
        'IOfilecheck':IOfilecheck,
        'timer':timer,
        #'windowrange':windowrange,
        #'distwindowrange':distwindowrange,
        'stitch':stitch,
        #'crop':crop,
        #'wc':wc,
        #'mask':mask,
        #'imagefilter':imagefilter,
        #'thickness':thickness,
        #'remove':remove,
        #'distmap':distmap,
        #'radwc':radwc
    }    
    
    for analysis in analysis_list:
        analysis_pos = analysis_pos_list[analysis]
        parameters = userconfiganalysis(wd, analysis_pos, analysis)
        if analysis == 'stitch':
            I = parameters['image_filename']
            O = parameters['output_filename']
        IOcheck = dispatch['IOfilecheck'](I, O)
        if not IOcheck == 10:
            print(analysis+' either has no input files, or already has output files.  Skipping...')
            if override == 1:
                print('overriding skip...')
                dispatch[analysis](parameters)
        else:
            dispatch[analysis](parameters)
    