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

def IOfilecheck(input_filename, output_filename):
    Icheck = 0
    Ocheck = 0
    if not os.path.isdir(input_filename):
        os.makedirs(input_filename)
    if not os.path.isdir(output_filename):
        os.makedirs(output_filename)
    
    if any(File.endswith('.fits') for File in os.listdir(input_filename)):
        Icheck = 1
    if any(File.endswith('.tiff') for File in os.listdir(input_filename)):
        Icheck = 1
    if any(File.endswith('.txt') for File in os.listdir(input_filename)):
        Icheck = 1
    
    if any(File.endswith('.fits') for File in os.listdir(output_filename)):
        Ocheck = 1
    if any(File.endswith('.tiff') for File in os.listdir(output_filename)):
        Ocheck = 1
    if any(File.endswith('.txt') for File in os.listdir(output_filename)):
        Ocheck = 1
    
    IOcheck = 10*Icheck + Ocheck
    
    return IOcheck