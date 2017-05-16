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
from windowrange import windowrange


def mask(parameters):
    '''
    SUMMARY: 
    'mask': creates binary segmented image from specified image using a local thresholding 
    technique.  
    
    USING CODE:
    For every pixel in the image, a surrounding window with size specified by 'windowsize'
    will be made, whereby an average value will be calculated.  If the difference between
    the evaluated pixel value and the average value is greater than the threshold, then the
    evaluated pixel will be considered True.  This code was written specifically with soil 
    roots in mind - therefore, roots will be expected to have a darker pixel value than the 
    surrounding dry soil, and will thereby be marked as True/white pixels.  
    
    PARAMETERS:
    1. image_filename: filename of evaluated image.  
    2. output_filename: filename where image is to be saved.
    3. windowsize: size of window.  Default is 101 pixels.
    4. threshold: minimum threshold against which image/average value difference will be 
    evaluated.  Default is 0.05.
    5. globthresh: value where if average pixel value in window is lower than, will automatically 
    set pixel to root.  This is to avoid a 'outline' effect where the center of thick roots will 
    be considered soil due to homogeneously dark pixel regions.  
    
    SAMPLE INPUT:
    
    ctype = 'Chamber2'

    wd_filename = '/Volumes/Untitled 2/rhizosphere'
    image_filename = wd_filename+'/stitched/'+ctype+'_stitched.fits'
    output_filename = wd_filename+'/masks/'+ctype+'_mask_nomorph.fits'

    windowsize = 101
    threshold = 0.05
    globthresh = 0.3
    
    '''
    
    starttime = time.time()
    scriptname = 'mask'
    
    timer.start(scriptname)
    
    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    windowsize = parameters['windowsize']
    threshold = parameters['threshold']
    globthresh = parameters['globthresh']
                               
    
    #image = fits.open(image_filename)[0].data
    image = Image.open(image_filename)
    image = np.array(image)
    
    
    mask = np.zeros([np.shape(image)[0],np.shape(image)[1]])
    L = (windowsize-1)/2
    imdim = np.shape(image)
    counter = 0
    pctval = 0
    totalcount = imdim[0]*imdim[1]

    
    for i in range(0,imdim[0]):
          for j in range(0,imdim[1]):
                [pctval,counter] = timer.progress(counter,pctval,totalcount)
                [y1,y2,x1,x2] = windowrange(i,j,windowsize,imdim)
                avgval = np.mean(image[y1:y2,x1:x2])
                if avgval <= globthresh:
                    mask[i,j] = 1
                    continue
                mask[i,j] = threshold < avgval-image[i,j]               
                   
    mask = Image.fromarray(mask)
    mask.save(output_filename)
    
    #imghdu = fits.PrimaryHDU(mask)
    #hdulist = fits.HDUList([imghdu])
    #hdulist.writeto(output_filename)
    
    timer.end(starttime)