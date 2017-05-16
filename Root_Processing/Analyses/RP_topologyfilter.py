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

from RP_timerstart import RP_timerstart
from RP_timerprogress import RP_timerprogress
from RP_timerend import RP_timerend
from RP_windowrange import RP_windowrange

def RP_topologyfilter(parameters):

    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    medfilterval = parameters['medfilterval']
    
    
    #image = fits.open(image_filename)[0].data
    image = Image.open(image_filename)
    image = np.array(image)
    
    image = medfilt(image, kernel_size = medfilterval)
    imdim = np.shape(image)
    
    img = image > 0
    mask_L = ndimage.measurements.label(img)
    mask_label = mask_L[0]
    
    #List of all labeled values
    labelcount = np.asarray(range(0,mask_L[1]+1))
    
    #Number of pixels per labeled object
    surface_areas = np.bincount(mask_label.flat)[0:]
    
    maxval = np.max(surface_areas[1:mask_L[1]+1])
    removedvals = np.zeros([mask_L[1]+1])

    for i in range(0, mask_L[1]+1):
        if not surface_areas[i] == maxval:
            removedvals[i] = 0
        else:
            #0 will be large due to background but needs to remain 0
            if labelcount[i] == 0:
                removedvals[i] = 0
            else:
                removedvals[i] = 1
    
    a = np.array(mask_label.flat)
    palette = labelcount
    key = removedvals
    
    index = np.digitize(a.ravel(), palette, right=True)
    imdim = np.shape(mask_label)
    img = key[index].reshape(imdim[0], imdim[1])
    
    img = Image.fromarray(img)
    img.save(output_filename)
    

    #imghdu = fits.PrimaryHDU(img)
    #hdulist = fits.HDUList([imghdu])
    #hdulist.writeto(output_filename)
    