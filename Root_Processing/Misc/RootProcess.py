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

def run(wd, filename, analyses, override, parameters = 0):
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
    
    if analyses == 'stitch':
        parameters_ = {'image_filename':wd+'/raw',
                       'output_filename':wd+'/stitched',
                       'fileformat':filename,
                      }        
    if analyses == 'wc':
        parameters_ = {'image_filename':wd+'/crop/'+filename+'_crop.fits',
                       'output_filename':wd+'/wc/'+filename+'_wc.fits'}
        
    if analyses == 'crop':
        parameters_ = {'image_filename':wd+'/stitched/'+filename+'_stitched.fits',
                       'output_filename':wd+'/crop/'+filename+'_crop.fits'}
        
    if analyses == 'mask':
        parameters_ = {'image_filename':wd+'/crop/'+filename+'_crop.fits',
                       'output_filename':wd+'/mask/'+filename+'_mask.fits'}  
        
    if analyses == 'imagefilter':
        parameters_ = {'image_filename':wd+'/mask/'+filename+'_mask.fits',
                       'output_filename':wd+'/mask_filter/'+filename+'_filter.fits'}
        
    if analyses == 'thickness':
        parameters_ = {'image_filename':wd+'/mask_filter/'+filename+'_filter.fits',
                       'output_filename':wd+'/thickness/'+filename+'_thickness.fits'}
        
    if analyses == 'distmap':
        parameters_ = {'image_filename':wd+'/mask_filter/'+filename+'_filter.fits',
                       'output_filename':wd+'/distmap/'+filename+'_distmap.fits'}
        
    if analyses == 'radwc':
        parameters_ = {'wc_filename':wd+'/wc/'+filename+'_wc.fits',
                       'distmap_filename':wd+'/distmap/'+filename+'_distmap.fits',
                       'mask_filename':wd+'/mask_filter/'+filename+'_filter.fits',
                       'output_filename':wd+'/radwc/'+filename,
                       'fileformat':filename}
    

    if not parameters == 0:
        parameters_ = {**parameters_,**parameters}

    if analyses == 'stitch':
        I = parameters_['image_filename']
        O = parameters_['output_filename']
    elif analyses == 'radwc':
        I = parameters_['wc_filename'].rsplit('/',1)[0]
        O = parameters_['output_filename']
    else:
        I = parameters_['image_filename'].rsplit('/',1)[0]
        O = parameters_['output_filename'].rsplit('/',1)[0]
    
    #print(analyses, end = ' ')
    #print(I, end = ' ')    
    IOcheck = IOfilecheck(I,O)
    
        
    if not IOcheck == 10:
        print(analyses+' either has no input files, or already has output files. Skipping...')
        if override == 1:
            print('overriding skip...')
            dispatch[analyses](**parameters_)
    else:            
        dispatch[analyses](**parameters_)
        
    


'''
Definitions that can be run for analysis (see below for details):
1. wc:
- REQUIRES: neutron transmission image (fits format, range from 0-1)
- PRODUCES: water content image (fits format)
- INPUT DIR: image name
- OUTPUT DIR: image name

2. mask:
- REQUIRES: neutron transmission image (fits format, range from 0-1)
- PRODUCES: binary mask image (fits format, range 0, 1)
- INPUT DIR: image name
- OUTPUT DIR: image name

3. thickness:
- REQUIRES: binary mask image (fits format, range 0, 1)
- PRODUCES: root thickness map (fits format)
- INPUT DIR: image name
- OUTPUT DIR: image name

4. distmap:
- REQUIRES: binary mask image (fits format, range 0, 1)
- PRODUCES: soil distance map (fits format)
- INPUT DIR: image name
- OUTPUT DIR: image name

5. radwc:
- REQUIRES: water content image, soil distance map, and mask image (all fits format)
NOTE: if run separately, user must specify all inputs
- PRODUCES: water content-radius text, wc-rad count, radius and distance values (text files) 
- INPUT DIR: image name
- OUTPUT DIR: text directory

Miscellaneous processing:
1. stitch:
- REQUIRES: original radiographs, open beam (labeled 'OB'), and dark field 
(labeled 'DF') images (fits format)
- PRODUCES: stitched neutron transmission image (fits format, range from 0-1)
- INPUT DIR: image directory
- OUTPUT DIR: image name

2. crop:
- REQUIRES: any image (fits format)
- PRODUCES: cropped version of image (fits format)
- INPUT DIR: image name
- OUTPUT DIR: image name

3. imagefilter:
- REQUIRES: original binary mask image (fits format, range 0, 1)
- PRODUCES: filtered mask image (fits format, range 0, 1)
- INPUT DIR: image name
- OUTPUT DIR: image name

- REQUIRES:
- PRODUCES:
- INPUT DIR:
- OUTPUT DIR:

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

def IOfilecheck(input_filename, output_filename):
    '''
    SUMMARY: 
    'IOfilecheck' confirms whether input and output file locations are prepared for processing.
    
    USING CODE:
    'IOfilecheck' is used to confirm whether there are files to be processed in the input file
    (specified by 'input_filename') and whether there are no files in the output file (specified by
    'output_filename'), and relayed back via 'IOcheck'.  If there is data in the input file but 
    none in the output file, then 'IOcheck' = 10, if there is data in both files, 'IOcheck' = 11, if
    there is data in the output but none in the input, 'IOcheck' = 1, and if there is no data in either,
    'IOcheck' = 0.
    
    PARAMETERS:
    A. INPUTS - 
    1. image_filename: filename where images are to be found.  
    2. output_filename: filename where image is to be saved.   
    
    B. OUTPUTS -
    1. IOcheck: flag indicating data presence in input/output file.
    '''
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

class timer:
    '''
    SUMMARY: 
    'timer' outputs script progress time.
    
    USING CODE:
    Depending on 'flag', code will operate under 'start', 'progress', or 'end' conditions.  
    'start' will output the 'scriptname' and '% complete' string, while 'progress' will output 
    the percentage and counter specified by 'counter', 'totalcount', and 'pctval', and 'end' 
    will output elapsed time.  

    NOTE: this is written specifically for the current processing routine, and is written with 
    an imaging context in mind.
    
    PARAMETERS:
    A. INPUTS -
    1. scriptname: the name of the script that the timer is being used for.
    2. counter: the number of counts at the current moment.  
    3. totalcount: the total number of counts to be measured.
    4. pctval: the current percentage value evaluated.
    5. starttime: the starting time of the code.
    6. flag: specifies which phase of the timer should be outputted.  Options are 'start', 
    'progress', and 'end'.
    
    B. OUTPUTS (only for 'progress') -
    1. pctval: the current percentage value, with progress added.
    2. counter: the current counter number, with progress added.
    '''
    
    def start(scriptname):
        print(scriptname+' - % complete: ', end=' ')
    
    def progress(counter, pctval, totalcount):
        if counter/totalcount >= pctval:
            print(round(100*pctval), end=' ')
            pctval += 0.01
            counter += 1
            return (pctval, counter)
        else:
            counter += 1
            return (pctval, counter)
            
    
    def end(starttime):
        print('\nElapsed time: {:0.1f} seconds.\n'.format(time.time()-starttime))
    

def windowrange(i,j,windowsize,imdim):
    '''
    SUMMARY:
    'windowrange': outputs rows/columns after considering edge effects based on current x/y
    position and image size.
    
    USING CODE: 
    Position 'i' (i.e. rows) and 'j' (i.e. columns) will be evaluated in conjunction with
    the evaluated window size 'windowsize', and ensure that the rows/columns outputted
    do not exceed image dimensions specified by 'imdim'.  Code will include last number
    to be excluded.  
    
    PARAMETERS: 
    A. INPUTS - 
    1. i: row position for the center of the window (y).
    2. j: column position for the center of the window (x).
    3. windowsize: 1D-size of the window.  Must be odd numbered. 
    4. imdim: image dimensions - row, column.
    
    B. OUTPUTS -
    1. y1: starting row position for evaluated window.
    2. y2: ending row position for evaluated window.
    3. x1: starting column position for evaluated window.
    4. x2: ending column position for evaluated window.
    
    
    EXAMPLE:
    For a 10x10 array and a window size of 3, evaluating a position at [5,6], 'i' and 
    'j' will correspond to 5 and 7, 'windowsize' will correspond to 3, and 'imdim' will
    correspond to [10, 10].  In this case, outputs will correspond to y1=2,y2=9,x1=3,x2=10.  
    
    If i and j were [7,8], then y1=4,y2=10,x1=5,x2=10.
    
    '''
    windowsize = np.floor(windowsize/2)
    
    y1 = i-windowsize
    y2 = i+windowsize+1
    if i < windowsize:
        y1 = 0
        y2 = i+windowsize+1
    elif i >= imdim[0]-windowsize:
        y1 = i-windowsize
        y2 = imdim[0]
    
    x1 = j-windowsize
    x2 = j+windowsize+1
    if j < windowsize:
        x1 = 0
        x2 = j+windowsize+1
    elif j >= imdim[1]-windowsize:
        x1 = j-windowsize
        x2 = imdim[1]
    
    y1 = int(y1)
    y2 = int(y2)
    x1 = int(x1)
    x2 = int(x2)
    
    return (y1,y2,x1,x2)

def distwindowrange(i,j,windowsize,imdim):
    '''
    SUMMARY:
    'distwindowrange':outputs rows/columns after considering edge effects for a single
    pixel distance array.  Used only in 'thickness' code.  
    
    USING CODE: 
    Position 'i' (i.e. rows) and 'j' (i.e. columns) will be evaluated in conjunction with 
    the evaluated window size 'windowsize', and ensure that the rows/columns outputted 
    do not exceed image dimensions specified by 'imdim'.  Code will include last number 
    to be excluded.  
    
    PARAMETERS: 
    A. INPUTS - 
    1. i: row position for the center of the window (y).
    2. j: column position for the center of the window (x).
    3. windowsize: 1D-size of the window.  Must be odd numbered. 
    4. imdim: image dimensions - row, column.
    
    B. OUTPUTS -
    1. y1: starting row position for evaluated window.
    2. y2: ending row position for evaluated window.
    3. x1: starting column position for evaluated window.
    4. x2: ending column position for evaluated window.
    5. yc: center row position for evaluated window.
    6. xc: center column position for evaluated window.
    
    
    EXAMPLE:
    For a 10x10 array and a window size of 3, evaluating a position at [5,6], 'i' and 
    'j' will correspond to 5 and 7, 'windowsize' will correspond to 3, and 'imdim' will 
    correspond to [10, 10].  In this case, outputs will correspond to y1=0,y2=8,x1=0,x2=8,yc=3,xc=3.  
    
    If i and j were [1,1], then y1=2,y2=8,x1=2,x2=8,yc=1,xc=1.
    '''
    
    windowsize = np.floor(windowsize/2)
    
    y1 = 0
    y2 = windowsize*2+2
    yc = windowsize
    
    if i < windowsize:
        y1 = windowsize-i
        yc = i
    elif i >= imdim[0]-windowsize:
        y2 = windowsize+(imdim[0]-i)+1
    
    x1 = 0
    x2 = windowsize*2+2
    xc = windowsize
    
    if j < windowsize:
        x1 = windowsize-j
        xc = j
    elif j >= imdim[1]-windowsize:
        x2 = windowsize+(imdim[1]-j)+1
        
    y1 = int(y1)
    y2 = int(y2)
    x1 = int(x1)
    x2 = int(x2)
    yc = int(yc)
    xc = int(xc)
        
    return (y1,y2,x1,x2,yc,xc)    

def stitch(image_filename, output_filename, fileformat, stitch_order, output_fileformat = 0,imdim = [2048, 2048], dimv_horzoffset=95, dimv_vertoffset=25, dimh_horzoffset=7, dimh_vertoffset=161, imformat = 'fits'):
    '''
    SUMMARY: 
    'stitch': creates combined image from specified multiple images.
    
    USING CODE: 
    'stitch_order' will specify the number of images, numbering scheme, and image position. 
    From the specified parameters, images located in 'image_filename' and labeled under the 
    general filename format 'fileformat' will be read in and positioned using the offset 
    variables specified in 'dimv_horzoffset', 'dimv_vertoffset', 'dimh_horzoffset', and 
    'dimh_vertoffset'.  The stitched image will then be outputted to 'output_filename' under
    the filename 'fileformat_stitched.fits'.  
    
    NOTE: Dark field and open beam images must be located in the same file, named 'DF.fits',
    and 'OB.fits', respectively.  Filenames will assume '%04d' format for numbering.  
    
    PARAMETERS:
    1. image_filename: filename where images are to be found.  
    2. output_filename: filename where image is to be saved.
    3. fileformat: filename format of the images.  Eg. For images labeled 'Scan_0001.fits',
    'Scan_0002.fits', etc., filename = 'Scan'.  
    4. stitch_order: array whose first two values indicate row and column number, and then
    following values specify what each column, by row, each image fits into.  
    example: img0-7 in a 2x4 r/c matrix format
           [4,5,6,7]
           [3,2,1,0]
     ---> stitch_order = [2,4,4,5,6,7,3,2,1,0]
    5. imdim: dimensions of the images to be stitched.  
    6-9. Offset values: 'dim_v' for images in vertical direction
    
    NOTE: all images in the row will be considered to have an equivalent offset, and all
    images in the column will be considered to have an equivalent offset.  

    img1: col B, row A
    img2: col A, row A
            __________
    _______|__       |
    |      | |       |
    |  img2| |  img1 |
    |      |_|_______|        
    |________|           |   <---- dimv_vertoffset

            _  <---- dimv_horzoffset



    img2: col A, row A
    img3: col A, row B

       ________
       |      |
       | img2 |
     __|_____ |
     | |____|_|    |   <---- dimh_vertoffset
     |      |
     | img3 |
     |______|


             _   <----- dimh_horzoffset


    SAMPLE INPUT:
    #Chamber 2_8: 8, post H2O w/ lamp

    image_filename = '/Volumes/Untitled 2/IPTS-14336/imgs/radiograph'
    output_filename = '/Volumes/Untitled 2/IPTS-14336/imgs/stitched'
    fileformat = 'Chamber2_8_'


    stitch_order = [4,4,63,62,61,60,70,69,68,67,77,76,75,74,84,83,82,81]

    dimv_horzoffset = 95
    dimv_vertoffset = 25
    dimh_horzoffset = 7
    dimh_vertoffset = 161


    '''
    
    starttime = time.time()
    scriptname = 'stitch'
    
    timer.start(scriptname)
    
    image_fn = image_filename+'/'+fileformat+'_'
    if output_fileformat == 0:   
        output_fn = output_filename+'/'+fileformat+'_stitched.'+imformat
    else:
        output_fn = output_filename+'/'+output_fileformat+'_stitched.fits'

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

    img = image[row_first:row_last,col_first:col_last]
    imghdu = fits.PrimaryHDU(img)
    hdulist = fits.HDUList([imghdu])
    hdulist.writeto(output_fn)
    
    timer.end(starttime)
    
def crop(image_filename, output_filename, cropmat = [0,0,0,0]):
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
    mask = fits.open(image_filename)[0].data
        
    imdim = np.shape(mask)
    
    if np.sum(cropmat) == 0:
        cropmat = [0, imdim[0], 0, imdim[1]]
        y = cropmat[0:2]
        x = cropmat[2:4]  
    else:
        y = cropmat[0:2]
        x = cropmat[2:4]
    
    mask = mask[int(imdim[0]-y[1]):int(imdim[0]-y[0]+1),int(x[0]):int(x[1]+1)]
    
    imghdu = fits.PrimaryHDU(mask)
    hdulist = fits.HDUList([imghdu])
    hdulist.writeto(output_filename)

    
def wc(image_filename, output_filename, b_w=-2.14,s_w=5.3,s_a=0.02015,s_s=0.006604,x_s=1,x_a=0.2):
    '''
    SUMMARY: 
    'wc': creates water content map from specified image using equations specified 
    in Kang et al., 2013.  
    
    USING CODE:
    Calculation assumes a uniform sandy (i.e. primarily Si) soil medium of thickness 'x_s', 
    with two thin sheets of aluminum with combined thickness 'x_a on each side.  Calculated 
    image is a total thickness of water in each pixel, which is then normalized by the 
    thickness of the pixel in total.  
    
    PARAMETERS:
    1. image_filename: filename of evaluated image. 
    2. output_filename: filename where image is to be saved.
    3. b_w: scattering coefficient of water [cm^-2]
    4. s_w: attenuation coefficient of water [cm^-1]
    5. s_a: attenuation coefficient of aluminum [cm^-1]
    6. s_s: attenuation coefficient of silicon [cm^-1]
    7. x_s: thickness of soil [cm]
    8. x_a: thickness of aluminum [cm]
    
    SAMPLE INPUT: 
    #Chamber 2
    wd_filename = '/Users/kdecarlo/Python_scripts'
    image_filename = wd_filename+'/stitched/Chamber10_inj_stitched.fits'
    output_filename = wd_filename+'/wc/Chamber10_inj_wc.fits'
    
    '''
    starttime = time.time()
    scriptname = 'wc'
    
    timer.start(scriptname)
    image = fits.open(image_filename)[0].data
    
    #Conversion from transmission data to water thickness [see Kang et al., 2013]
    C1 = s_w/(2*b_w)
    C2_s = s_a*x_s+s_s*x_s

    image[image == 0] = 'nan'
    x = C1*C1-(np.log(image)-C2_s)/b_w
    maskneg = np.isnan(x)
    np.shape(maskneg)
    x[np.isnan(x)] = 0
    x[x < 0] = 0

    x_w = -C1 - np.sqrt(x)
    x_w[x_w == -C1] = 'nan'
    x_w = x_w

    imghdu = fits.PrimaryHDU(x_w)
    hdulist = fits.HDUList([imghdu])
    hdulist.writeto(output_filename)
    timer.end(starttime)
    
    
def imagefilter(image_filename, output_filename, bwareaval=800, medfilterval=5):
    '''
    SUMMARY: 
    'imagefilter': conducts a simple filtering process of an image for later processing.
    
    USING CODE:
    Image located in 'image_filename' will be read in and will be converted into a binary image,
    after which a median filter will be applied with a windowsize specified in 'medfilterval'.  
    From that image, an area filter will be applied - all 'True' pixels with a total pixel count 
    higher than 'bwareaval' will be removed from the image.  
    
    
    PARAMETERS:
    1. image_filename: filename of evaluated image. 
    2. output_filename: filename where image is to be saved.
    3. bwareaval: scalar value of the minimum pixel count (i.e. area) to be removed.
    4. medfilterval: window size to be used in the median filter.
    
    SAMPLE INPUT: 
    #Chamber 2
    wd_filename = '/Users/kdecarlo/Python_scripts'
    image_filename = wd_filename+'/stitched/Chamber10_inj_stitched.fits'
    output_filename = wd_filename+'/wc/Chamber10_inj_wc.fits'
    bwareaval = 800
    medfilterval = 5
    
    '''
    
    image = fits.open(image_filename)[0].data
    image = medfilt(image, kernel_size = medfilterval)
    imdim = np.shape(image)
    
    img = image > 0
    mask_L = ndimage.measurements.label(img)
    mask_label = mask_L[0]
    
    #List of all labeled values
    labelcount = np.asarray(range(0,mask_L[1]+1))
    
    #Number of pixels per labeled object
    surface_areas = np.bincount(mask_label.flat)[0:]
    
    #labels to be converted to 0 - same size as label list, but all 
    #replaced values changed to 0
    removedvals = np.zeros([mask_L[1]+1])
    for i in range(0,mask_L[1]+1):
        if surface_areas[i] <= bwareaval:
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

    imghdu = fits.PrimaryHDU(img)
    hdulist = fits.HDUList([imghdu])
    hdulist.writeto(output_filename)
    
    
def mask(image_filename, output_filename, windowsize=101, threshold=0.05, globthresh=0.3):
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
    
    image = fits.open(image_filename)[0].data
    
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
                   
    imghdu = fits.PrimaryHDU(mask)
    hdulist = fits.HDUList([imghdu])
    hdulist.writeto(output_filename)
    
    timer.end(starttime)

def thickness(image_filename, output_filename):
    '''
    SUMMARY:
    'thickness': creates a half-thickness image from a binary segmented image of a root, 
    assuming a cylindrical shape.
    
    USING CODE:
    Using the binary image, a skeleton (i.e. medial axis transform) of the original image 
    is calculated.  A distance transform of the root is then calculated.  
    
    From here, for every pixel (x,y)_p, the following are calculated: (1) a minimum 
    distance from the pixel to a medial axis pixel (x, y)_m (i.e. skeleton), from which 
    the distance transform value (i.e. radius R) is extracted; and (2) a minimum distance 
    L_e from the pixel to the root edge (x,y)_e.  Then, assuming a cylindrical distribution, 
    and also assuming that the differences in slopes of lines ep and pm are negligible, 
    the half-dome height H of the pixel is calculated as follows: T^2 = R^2-(R-EP)^2.   
    
    PARAMETERS:
    1. image_filename: filename of evaluated image.  
    2. output_filename: filename where image is to be saved.
    
    SAMPLE INPUT: 
    ctype = 'Chamber10'
    
    wd_filename = '/Volumes/Untitled 2/rhizosphere'
    image_filename = wd_filename+'/morph_mask_crop/clean/'+ctype+'_clean.tif'
    output_filename = wd_filename+'/thickness/'+ctype+'_radmap.fits'
    
    '''
    
    starttime = time.time()
    scriptname = 'thickness map'

    timer.start(scriptname)

    #image = Image.open(image_filename)
    image = fits.open(image_filename)[0].data

    image = medfilt(image, kernel_size = 7)
    imdim = np.shape(image)

    #image = np.asarray(image)
    #Skeletonization of root image
    skel = skeletonize(image > 0)

    #Distance transform from center of root to all other pixels
    #dist = ndimage.morphology.distance_transform_edt(~skel)

    #Distance from edge of root to center
    rootdist = ndimage.morphology.distance_transform_edt(image)

    checkwin = int(np.round(np.max(rootdist)*1.5))
    checkwindow = 11
    while checkwindow < checkwin:
        checkwindow += 2

    #Reference distance map for evaluated windows
    windist = np.ones([checkwindow*2+1,checkwindow*2+1])
    windist[checkwindow,checkwindow] = 0
    windist = ndimage.morphology.distance_transform_edt(windist)
    
    [pixelpos_y,pixelpos_x] = np.where(image > 0)

    T_map = np.zeros(imdim)
    counter = 0
    pctval = 0
    totalcount = np.shape(pixelpos_x)[0]

    for m in range(0,np.shape(pixelpos_x)[0]):
        [pctval,counter] = timer.progress(counter,pctval,totalcount)

        i = pixelpos_y[m]
        j = pixelpos_x[m]

        [y1,y2,x1,x2] = windowrange(i,j,np.shape(windist)[0],imdim)
        [y_1,y_2,x_1,x_2,y_c,x_c] = distwindowrange(i,j,np.shape(windist)[0],imdim)

        windist_w = windist[y_1:y_2,x_1:x_2]
        image_w = image[y1:y2,x1:x2]
        #dist_w = dist[y1:y2,x1:x2]
        skel_w = skel[y1:y2,x1:x2]
        rootdist_w = rootdist[y1:y2,x1:x2]


        #Find minimum distance from pixel of interest to skeleton
        skelpos = np.where(skel_w)
        skelpos_y = skelpos[0]
        skelpos_x = skelpos[1]
        skeldist = np.zeros([np.shape(skelpos_y)[0]])
        for k in range(np.shape(skelpos_y)[0]):
            skeldist[k] = np.sqrt((y_c-skelpos_y[k])*(y_c-skelpos_y[k]) + (x_c-skelpos_x[k])*(x_c-skelpos_x[k]))
            minskelpos = np.where(skeldist == np.min(skeldist))
            minskelpos_y = skelpos_y[minskelpos[0][0]]
            minskelpos_x = skelpos_x[minskelpos[0][0]]
            dist_pixel_skel = skeldist[minskelpos[0][0]]

            #Find minimum distance from pixel of interest to edge
            dist_pixel_edge = rootdist_w[y_c,x_c]
            rad_val = rootdist_w[minskelpos_y,minskelpos_x]

            #Calculate thickness
            T_map[i,j] = np.sqrt(rad_val*rad_val-(rad_val-dist_pixel_edge)*(rad_val-dist_pixel_edge))

    imghdu = fits.PrimaryHDU(T_map)
    hdulist = fits.HDUList([imghdu])
    hdulist.writeto(output_filename)
    timer.end(starttime)
    
                                 
    
def remove(image, connection=4,edge=True):
    '''
    SUMMARY: 
    'remove': creates a contour image of the original by removing all center pixels.  
    
    USING CODE:
    The inputted binary image will be checked at all true pixels to confirm 4- or 8-connection.
    If valid, then this pixel will be considered a non-contour pixel and not included.  'edge' 
    affirms whether any objects that terminate on the edge of the image should be considered 
    'closed' (i.e. fully within the image) or 'open' (i.e. continues outside
    the image) object.  If the object is considered 'open' (i.e. True), then the contour pixels
    will not fully wrap around the object.
    
    PARAMETERS:
    1. image: binary image to be analyzed.
    2. connection: scalar value that specifies what connection to be used.  Either 4 or 8 is valid.
    3. edge: flag confirming whether objects on edge of image are considered 'open' or 'closed'.
    Takes values of 'TRUE' (open) or 'FALSE' (closed).
    
    '''

    imagepos = np.where(image)
    imagepos_y = imagepos[0]+1
    imagepos_x = imagepos[1]+1
    
    imdim = np.shape(image)
    if edge:
        img = np.ones([imdim[0]+2, imdim[1]+2])
    else:
        img = np.zeros([imdim[0]+2, imdim[1]+2])
    
    finalimg = np.zeros([imdim[0]+2,imdim[1]+2])
    img[1:imdim[0]+1,1:imdim[1]+1] = image
    
    if connection == 4:
        for i in range(np.shape(imagepos_y)[0]):
            x = imagepos_x[i]
            y = imagepos_y[i]
            if (img[y-1,x]+img[y+1,x]+img[y,x-1]+img[y,x+1]) == 4:
                continue
            else:
                finalimg[y,x] = 1
    
    if connection == 8:
        for i in range(np.shape(imagepos_y)[0]):
            x = imagepos_x[i]
            y = imagepos_y[i]
            if (img[y-1,x]+img[y+1,x]+np.sum(img[y-1:y+2,x-1])+np.sum(img[y-1:y+2,x+1])) == 8:
                continue
            else:
                finalimg[y,x] = 1
    
    finalimg = finalimg[1:imdim[0]+1,1:imdim[1]+1]
    
    return finalimg


def distmap(image_filename, output_filename, maxval = 400):
    '''
    SUMMARY: 
    'distmap': associates every soil pixel with an associated root diameter.
    
    USING CODE:
    From the binary root image located in 'image_filename', a contour image (using 
    RootProcess.remove) and a skeletonized radius image will be made.  The skeletonized
    radius image is made by creating a medial axis transform (i.e. skeleton) of the 
    binary image.
    
    Processing is conducted in two stages: in stage one, every contour pixel is associated
    with a radius pixel via closest distance.  In stage two, every soil pixel is then
    associated with a contour pixel via closest distance.  Due to possibly very large sizes and 
    lack of interest in far away soil pixels, a 'maxval' which sets the maximum distance of the
    soil pixel from the root to be evaluated.
        
        
    PARAMETERS:
    1. image_filename: filename of evaluated image.  
    2. output_filename: filename where image is to be saved.
    3. maxval: maximum soil-pixel/root edge-pixel distance, beyond which soil pixels will not 
    be calculated.
    
    '''
    
    
    starttime = time.time()
    scriptname = 'distmap: contours'
    
    timer.start(scriptname)
    
    image = fits.open(image_filename)[0].data
    #image = Image.open(image_filename)
    image = np.array(image)
    image = image > 0
    
    #1. Find edge/contour of roots
    contour_img = remove(image)
    
    #2. ID all non-root pixels
    soilmap = image < 1
    
    #3. Create radius-labeled skeleton (medial axis) of root
    skel = skeletonize(image)
    skel = skel > 0
    rootdist = ndimage.morphology.distance_transform_edt(image)
    rootdist[~skel] = 0
    
    #4. ID position of all contour pixels
    contourpos = np.where(contour_img)
    contourpos_y = contourpos[0]
    contourpos_x = contourpos[1]
    
    #5. ID position of all skeleton pixels
    skelpos = np.where(skel)
    skelpos_y = skelpos[0]
    skelpos_x = skelpos[1]
    
    #6. Contour map where each contour pixel corresponds to closest medial axis
    contour_skel_map = np.zeros(np.shape(image))
    
    #9. ID all soil pixels
    pixelpos = np.where(soilmap)
    pixelpos_y = pixelpos[0]
    pixelpos_x = pixelpos[1]
    
    distmapvals = ndimage.morphology.distance_transform_edt(~image)
    
    
    #9. ID all soil pixels
    if maxval == 'all':
        pixelpos = np.where(soilmap == True)
    else:
        pixelpos = np.where((distmapvals < maxval) & (soilmap == True))
    
    pixelpos_y = pixelpos[0]
    pixelpos_x = pixelpos[1]        

    imdim = np.shape(image)
    
    counter = 0
    pctval = 0
    totalcount = np.shape(contourpos_y)[0]
    
    
    #7. Loop through all contour pixels
    for i in range(np.shape(contourpos_y)[0]):
        [pctval,counter] = timer.progress(counter,pctval,totalcount)

        y = contourpos_y[i]
        x = contourpos_x[i]
    
        #Find distance between pixel and all skeleton pixels
        check = np.sqrt((skelpos_y-y)*(skelpos_y-y)+(skelpos_x-x)*(skelpos_x-x))
        minpos = np.where(check == check.min())
        #ID closest skeleton pixel
        yc = skelpos_y[minpos[0][0]]
        xc = skelpos_x[minpos[0][0]]

        #place in contour-skel map
        contour_skel_map[y,x] = rootdist[yc,xc]
    
    #8. Soil map where each soil pixel corresponds to closest medial axis
    soil_contour_map = np.zeros(np.shape(image))
    
    timer.end(starttime)

    
    starttime = time.time()
    scriptname = 'distmap: soil dist'
    
    timer.start(scriptname)
    
    
    
    counter = 0
    pctval = 0
    totalcount = np.shape(pixelpos_y)[0]
    
    
    for i in range(np.shape(pixelpos_y)[0]):
        [pctval,counter] = timer.progress(counter,pctval,totalcount)

        y = pixelpos_y[i]
        x = pixelpos_x[i]
        
        
        distval = distmapvals[y,x]
        windowsize = 2*(np.floor(distval)+1)

        [y1,y2,x1,x2] = windowrange(y,x,windowsize,imdim)


        contour_w = contour_skel_map[y1:y2,x1:x2]

        contourpos_w = np.where(contour_w)
        contourpos_w_y = contourpos_w[0]
        contourpos_w_x = contourpos_w[1]

        check = np.sqrt((contourpos_w_y-y)*(contourpos_w_y-y)+(contourpos_w_x-x)*(contourpos_w_x-x))
        minpos = np.where(check == check.min())
        yc = contourpos_w_y[minpos[0][0]]
        xc = contourpos_w_x[minpos[0][0]]

        val = contour_w[yc,xc]

        soil_contour_map[y,x] = val
  
    imghdu = fits.PrimaryHDU(soil_contour_map)
    hdulist = fits.HDUList([imghdu])
    hdulist.writeto(output_filename)
    
    timer.end(starttime)

def radwc(wc_filename, distmap_filename, mask_filename, output_filename, fileformat, pixelbin = 3):
    '''
    SUMMARY:
    'radwc': creates two NxM text files of the water content of a given root radius (row) at a given distance
    from the root (column), and the number of pixels for each entry, as well as a 1xN and 1xM text file of 
    the root radius values and distance from the root, respectively.  All distance and radius values are 
    outputted in terms of pixels.
    
    USING CODE:
    Necessary images are the water content image (located in 'wc_filename'), the soil-distance map
    created by 'RootProcess.distmap' (located in 'distmap_filename'), and the binary root mask 
    (located in 'mask_filename').  'output_filename' specifies the folder where all files will be placed.
    'fileformat' specifies the name of the file.  The water content for each root radius at a given distance
    will be labeled "fileformat+'_data_xrad_ydist_wc.txt'", the numerical counts as "fileformat+'data_num_xrad'
    +'_ydist_wc.txt'", the y axis (i.e. root radius values) will be labeled "fileformat"+'_data_radrange.txt'", 
    and the x axis (i.e. distance values) will be labeled "fileformat+'_data_distrange.txt'".  So, for example,
    if 'fileformat' = 'Test', then the water content data will be labeled 'Test_data_xrad_ydist_wc.txt'.  
    
    'pixelbin' specifies the number of pixels to be binned on the distance axis, with a default of 3 pixels
    per bin.  
    
    PARAMETERS:
    1. wc_filename: filename of the water content image.  
    2. distmap_filename: filename of the distance map image.
    3. mask_filename: filename of the root mask image.
    4. output_filename: filename where the text files are to be saved.
    5. fileformat: the filename prefix to be attached to the data.
    6. pixelbin: the number of pixels to be binned when determining water contents by distance.
    
    SAMPLE:
    cmat = ['Chamber1', 'Chamber2', 'Chamber3']
    wc_filename = wd_filename+'/wc/'+cmat[0]+'_wc.fits'
    distmap_filename = wd_filename+'/distmap/'+cmat[0]+'_distmap.fits'
    mask_filename = wd_filename+'/filter/'+cmat[0]+'_filter.fits'
    output_filename = wd_filename+'/rhizosphere_data/'+cmat[0]
    fileformat = cmat[0]
    pixelbin = 3

    '''

    starttime = time.time()
    scriptname = 'radwc'
    
    timer.start(scriptname)
    
    image_wc = fits.open(wc_filename)[0].data
    image_distmap = fits.open(distmap_filename)[0].data
    image_mask = fits.open(mask_filename)[0].data
    image_mask = image_mask > 0
    image_rootdist = ndimage.morphology.distance_transform_edt(~image_mask)

    soilmap = image_mask < 1

    pixelpos = np.where(soilmap)
    pixelpos_y = pixelpos[0]
    pixelpos_x = pixelpos[1]

    data = np.zeros([np.shape(pixelpos_y)[0], 3])

    radrange = np.unique(image_distmap)
    distrange = np.unique(image_rootdist)
    maxdistval = np.max(distrange)
    maxradval = np.max(radrange)
    newdistrange = np.array(range(0, int(np.floor(maxdistval)), pixelbin))

    data = np.zeros([int(np.shape(radrange)[0])-1, np.shape(range(0,int(np.floor(maxdistval)), pixelbin))[0]])
    data_num = np.zeros([int(np.shape(radrange)[0])-1, int(np.shape(range(0,int(np.floor(maxdistval)), pixelbin))[0])])
    
    counter = 0
    pctval = 0
    totalcount = np.shape(data)[0]*np.shape(data)[1]

    outline_img = remove(image_mask)
    image_mask_wooutline = image_mask > 0
    image_mask_wooutline[outline_img > 0] = False

    image_rootdist[image_mask_wooutline] = -1
    

    for i in range(0,np.shape(newdistrange)[0]-1):
        for j in range(1,np.shape(radrange)[0]):
            [pctval,counter] = timer.progress(counter,pctval,totalcount)
            
            image_pos = (image_rootdist >= newdistrange[i]) & (image_rootdist < newdistrange[i+1]) & (image_distmap == radrange[j])
            if np.sum(image_pos) > 0:
                data[j-1,i] = np.mean(image_wc[image_pos])
                data_num[j-1,i] = np.sum(image_pos)
            
            
    np.savetxt(output_filename+'/'+fileformat+'_data_xrad_ydist_wc.txt', data)
    np.savetxt(output_filename+'/'+fileformat+'_data_num_xrad_ydist_wc.txt', data_num)
    np.savetxt(output_filename+'/'+fileformat+'_data_radrange.txt', radrange[1:np.shape(radrange)[0]])
    np.savetxt(output_filename+'/'+fileformat+'_data_distrange.txt', newdistrange)