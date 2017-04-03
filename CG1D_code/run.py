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
from crop import crop
from wc import wc
from mask import mask
from maskfilter import maskfilter
from distmap import distmap
from radwc import radwc
from thickness import thickness
from userconfiganalysis import userconfiganalysis
from windowrange import windowrange
from distwindowrange import distwindowrange

def run(wd, analysis_list, override = 0):
    
    #User config analysis positions:
    analysis_pos_list = {
        'stitch':[2,10],
        'crop':[13,15],
        'wc':[18,25], 
        'mask':[28,32],
        'maskfilter':[35,38],
        'distmap':[41,43],
        'radwc':[46,51],
        'thickness':[54,55]
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
        'radwc':radwc
    }    
    
    for analysis in analysis_list:
        analysis_pos = analysis_pos_list[analysis]
        parameters = userconfiganalysis(wd, analysis_pos, analysis)
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
    