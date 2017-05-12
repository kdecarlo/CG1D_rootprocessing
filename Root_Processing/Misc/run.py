import numpy as np
from astropy.io import fits
import time
import scipy.ndimage as imp
import datetime

from scipy import ndimage
#from skimage.morphology import skeletonize
import scipy.misc
from scipy.signal import medfilt
from PIL import Image
import os
import sys






def run(wd, analysis_list, parameters_ = 0, override = 0):
    
    sys.path.append(wd+'/Analyses')
    sys.path.append(wd+'/Misc')
    
    from IOfilecheck import IOfilecheck
    from timerstart import timerstart
    from timerprogress import timerprogress
    from timerend import timerend
    from stitch import stitch
    from crop import crop
    from wc import wc
    from mask import mask
    from imagefilter import imagefilter
    from distmap import distmap
    from radwc import radwc
    from thickness import thickness
    from userconfiganalysis import userconfiganalysis
    from windowrange import windowrange
    from distwindowrange import distwindowrange
    from remove import remove
    from topologyfilter import topologyfilter
    
    '''
    Definitions that can be run for analysis (see below for details):
    1. wc:
    - REQUIRES: neutron transmission image (fits format, range from 0-1)
    - PRODUCES: water content image (fits format)

    2. mask:
    - REQUIRES: neutron transmission image (fits format, range from 0-1)
    - PRODUCES: binary mask image (fits format, range 0, 1)

    3. thickness:
    - REQUIRES: binary mask image (fits format, range 0, 1)
    - PRODUCES: root thickness map (fits format)

    4. distmap:
    - REQUIRES: binary mask image (fits format, range 0, 1)
    - PRODUCES: soil distance map (fits format)

    5. radwc:
    - REQUIRES: water content image, soil distance map, and mask image (all fits format)
    NOTE: if run separately, user must specify all inputs
    - PRODUCES: water content-radius text, wc-rad count, radius and distance values (text files) 

    Miscellaneous processing:
    1. stitch:
    - REQUIRES: original radiographs, open beam (labeled 'OB'), and dark field 
    (labeled 'DF') images (fits format)
    - PRODUCES: stitched neutron transmission image (fits format, range from 0-1)

    2. crop:
    - REQUIRES: any image (fits format)
    - PRODUCES: cropped version of image (fits format)

    3. imagefilter:
    - REQUIRES: original binary mask image (fits format, range 0, 1)
    - PRODUCES: filtered mask image (fits format, range 0, 1)

    Full list of definitions:

    IOfilecheck
    timer
    windowrange
    distwindowrange
    stitch
    crop
    wc
    mask
    thickness
    remove
    distmap
    radwc

    '''
    
    
    #User config analysis positions:
    analysis_pos_list = {
        'stitch':[2,10],
        'crop':[13,15],
        'wc':[18,25], 
        'mask':[28,32],
        'maskfilter':[35,38],
        'distmap':[41,43],
        'radwc':[46,51],
        'thickness':[54,55],
        'topologyfilter':[58,60]
    }
    
    
    
    #Dispatch
    dispatch = {
        'IOfilecheck':IOfilecheck,
        'timer':timer,
        'windowrange':windowrange,
        'distwindowrange':distwindowrange,
        'stitch':stitch,
        'crop':crop,
        'wc':wc,
        'mask':mask,
        'imagefilter':imagefilter,
        'thickness':thickness,
        'remove':remove,
        'distmap':distmap,
        'radwc':radwc,
        'topologyfilter':topologyfilter
    }    
    
    for analysis in analysis_list:
        analysis_pos = analysis_pos_list[analysis]
        parameters = userconfiganalysis(wd, analysis_pos, analysis)
        if not parameters_ == 0:
            parameters = {**parameters, **parameters_}
            
        if analysis == 'stitch':
            I = parameters['image_filename']
            O = parameters['output_filename']
        elif analysis == 'radwc':
            I = parameters_['wc_filename'].rsplit('/',1)[0]
            O = parameters_['output_filename']
        else:
            I = parameters['image_filename'].rsplit('/',1)[0]
            O = parameters['output_filename'].rsplit('/',1)[0]
            
        IOcheck = dispatch['IOfilecheck'](I, O)
        
        if not IOcheck == 10:
            print(analysis+' either has no input files, or already has output files.  Skipping...')
            if override == 1:
                override_val = override*100+IOcheck
                print('overriding skip...')
                dispatch[analysis](parameters)
        else:
            dispatch[analysis](parameters)
    