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

def stitch(parameters):
    starttime = time.time()
    scriptname = 'stitch'
    
    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    stitch_order = parameters['stitch_order']
    fileformat = parameters['fileformat']
    dimh_horzoffset = parameters['dimh_horzoffset']
    dimh_vertoffset = parameters['dimh_vertoffset']
    dimv_horzoffset = parameters['dimv_horzoffset']
    dimv_vertoffset = parameters['dimv_vertoffset']
    output_fileformat = parameters['output_fileformat']
    
    imformat = 'tiff'
    
    timer.start(scriptname)
    
    image_fn = image_filename+'/'+fileformat+'_'
    if output_fileformat == 0:   
        output_fn = output_filename+'/'+fileformat+'_stitched.'+imformat
    else:
        output_fn = output_filename+'/'+output_fileformat+'_stitched.'+imformat

    so = stitch_order
    stitch_order = np.zeros([int(so[0]),int(so[1])])
    

    counter = 2
    for i in range(0,so[0]):
        for j in range(0,so[1]):
            stitch_order[i,j] = so[counter]
            counter += 1
    #Read in OB/DF images
    OB_filename = image_filename+'/OB.'+imformat
    DF_filename = image_filename+'/DF.'+imformat
    
    if imformat == 'fits':
        ##DF
        DF = fits.open(DF_filename)[0].data
        ##OB
        OB = fits.open(OB_filename)[0].data-DF
    elif imformat == 'tiff':
        DF = Image.open(DF_filename)
        OB = Image.open(OB_filename)
        DF = np.flipud(DF)
        OB = np.flipud(OB)


        
    imdim = [2048, 2048]
    #Read in images and stitch them into master image
    dimval = np.shape(stitch_order)

    ##Define row and col positions for each image
    dimval = np.shape(stitch_order)
    rowvals = np.zeros([dimval[0]*dimval[1]])
    colvals = np.zeros([dimval[0]*dimval[1]])
    rowvals[0] = int(np.round(((dimval[0]-1)+0.25)*imdim[0]))
    colvals[0] = int(np.round(0.25*imdim[1]))

    stitch_list = np.zeros([dimval[0]*dimval[1]])

    
    counter = 0
    for i in range(0,dimval[0]):
        for j in range(0,dimval[1]):
            stitch_list[counter] = stitch_order[i,j]
            if i+j==0:
                counter += 1
                continue
            rowvals[counter] = rowvals[0]-i*(imdim[0]-dimh_vertoffset)+j*dimv_vertoffset
            colvals[counter] = colvals[0]+j*(imdim[0]-dimv_horzoffset)-i*dimh_horzoffset
            counter += 1

    image = np.zeros([int(np.round((dimval[0]+0.5)*imdim[0])), int(np.round(((dimval[1]+0.5)*imdim[1])))])
    np.shape(image)
    counter = 1
            
    for i in range(0,dimval[0]*dimval[1]):
        so = int(stitch_list[i])
        
        #print(so, end = ' ')
        #print(type(so), end = ' ')
        
        filename = image_fn+'%04d' %so
        filename = filename+'.'+imformat
        counter += 1
        #print(filename)
        if imformat == 'fits':
            img = fits.open(filename)[0].data-DF
        elif imformat == 'tiff':
            img = Image.open(filename)
            img = np.flipud(img)
        img = np.divide(img, OB)
        image[int(rowvals[i]):int(rowvals[i]+imdim[0]),int(colvals[i]):int(colvals[i]+imdim[1])] = img

    #row cutting
    img_row = np.zeros([np.shape(image)[0]])
    img_col = np.zeros([np.shape(image)[1]])
    for i in range(0,np.shape(image)[0]):
        img_row[i] = np.sum(image[i,0:np.shape(image)[1]])

    #column cutting    
    for i in range(0,np.shape(image)[1]):
        img_col[i] = np.sum(image[0:np.shape(image)[0],i])

    row_first = np.nonzero(img_row)[0][0]
    row_last = np.nonzero(img_row)[0][np.shape(np.nonzero(img_row)[0])[0]-1]
    col_first = np.nonzero(img_col)[0][0]
    col_last = np.nonzero(img_col)[0][np.shape(np.nonzero(img_col)[0])[0]-1]

    if imformat == 'fits':
        img = image[row_first:row_last,col_first:col_last]
        imghdu = fits.PrimaryHDU(img)
        hdulist = fits.HDUList([imghdu])
        hdulist.writeto(output_fn)
    elif imformat == 'tiff':
        img = image[row_first:row_last,col_first:col_last]
        img = np.flipud(img)
        img = Image.fromarray(img)
        img.save(output_fn)

        #scipy.misc.imsave(output_fn, img)
    
    timer.end(starttime)