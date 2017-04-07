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

from timer import timer

def crop(parameters):
    '''
    SUMMARY:
    'crop': crops image.
    
    USING CODE:
    Using values in 'cropvals' (start row, end row, start col, end col), image is 
    cropped down.  Note that row and col values correspond to x/y positions in ImageJ.  
    
    PARAMETERS: 
    1. image_filename: filename of evaluated image.
    2. output_filename: filename where image is to be saved.
    3. cropvals: 4x1 array specifying crop range - (1) start row, (2) end row, 
    (3) start column, (4) end column.  
    
    SAMPLE INPUT:
    ctype = 'Chamber2'
    wd_filename = '/Volumes/Untitled 2/rhizosphere'
    image_filename = wd_filename+'/stitched/'+ctype+'_stitched.fits'
    output_filename = wd_filename+'/morph_mask_crop/'+ctype+'_stitched_crop.fits'
    cropmat = [96,2848,1248,6384]
    '''
    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    cropmat = parameters['cropmat']
        
    mask = Image.open(image_filename)
    
    mask = np.array(mask)
    
    imdim = np.shape(mask)
    
    if np.sum(cropmat) == 0:
        cropmat = [0, imdim[0], 0, imdim[1]]
        y = cropmat[0:2]
        x = cropmat[2:4]  
    else:
        y = cropmat[0:2]
        x = cropmat[2:4]
    
    mask = mask[int(imdim[0]-y[1]):int(imdim[0]-y[0]+1),int(x[0]):int(x[1]+1)]
    mask = Image.fromarray(mask)
    mask.save(output_filename)
    
    
    #scipy.misc.imsave(output_filename, mask)