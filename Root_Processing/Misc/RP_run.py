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






def RP_run(wd, analysis_list, parameters_ = 0, override = 0):
    
    sys.path.append(wd+'/Analyses')
    sys.path.append(wd+'/Misc')
    
    from RP_IOfilecheck import RP_IOfilecheck
    from RP_timerstart import RP_timerstart
    from RP_timerprogress import RP_timerprogress
    from RP_timerend import RP_timerend
    from RP_stitch import RP_stitch
    from RP_crop import RP_crop
    from RP_wc import RP_wc
    from RP_mask import RP_mask
    from RP_imagefilter import RP_imagefilter
    from RP_distmap import RP_distmap
    from RP_radwc import RP_radwc
    from RP_thickness import RP_thickness
    from RP_userconfiganalysis import RP_userconfiganalysis
    from RP_windowrange import RP_windowrange
    from RP_distwindowrange import RP_distwindowrange
    from RP_remove import RP_remove
    from RP_topologyfilter import RP_topologyfilter
    
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
        'RP_stitch':[2,10],
        'RP_crop':[13,15],
        'RP_wc':[18,25], 
        'RP_mask':[28,32],
        'RP_maskfilter':[35,38],
        'RP_distmap':[41,43],
        'RP_radwc':[46,51],
        'RP_thickness':[54,55],
        'RP_topologyfilter':[58,60]
    }
    
    
    
    #Dispatch
    dispatch = {
        'RP_IOfilecheck':RP_IOfilecheck,
        'RP_timerstart':RP_timerstart,
        'RP_timerprogress':RP_timerprogress,
        'RP_timerend':RP_timerend,
        'RP_windowrange':RP_windowrange,
        'RP_distwindowrange':RP_distwindowrange,
        'RP_stitch':RP_stitch,
        'RP_crop':RP_crop,
        'RP_wc':RP_wc,
        'RP_mask':RP_mask,
        'RP_imagefilter':RP_imagefilter,
        'RP_thickness':RP_thickness,
        'RP_remove':RP_remove,
        'RP_distmap':RP_distmap,
        'RP_radwc':RP_radwc,
        'RP_topologyfilter':RP_topologyfilter
    }    
    
    for analysis in analysis_list:
        analysis_pos = analysis_pos_list[analysis]
        parameters = RP_userconfiganalysis(wd, analysis_pos, analysis)
        if not parameters_ == 0:
            parameters = {**parameters, **parameters_}
            
        if analysis == 'RP_stitch':
            I = parameters['image_filename']
            O = parameters['output_filename']
        elif analysis == 'RP_radwc':
            I = parameters_['wc_filename'].rsplit('/',1)[0]
            O = parameters_['output_filename']
        else:
            I = parameters['image_filename'].rsplit('/',1)[0]
            O = parameters['output_filename'].rsplit('/',1)[0]
            
        IOcheck = dispatch['RP_IOfilecheck'](I, O)
        
        if not IOcheck == 10:
            print(analysis+' either has no input files, or already has output files.  Skipping...')
            if override == 1:
                override_val = override*100+IOcheck
                print('overriding skip...')
                dispatch[analysis](parameters)
        else:
            dispatch[analysis](parameters)
    