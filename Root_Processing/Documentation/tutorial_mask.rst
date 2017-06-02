.. tutorial_mask:

************************
Getting Started: mask
************************

**I. OVERVIEW**

The 'RP_mask' analysis creates a binary segmented image from a specified image using a simple local thresholding technique.

In this analysis, each pixel will have an associated window of pixels in all directions.  From this window, a mean pixel value will be calculated

.. figure:: _static/maskval.jpg
   :scale: 100 %
   :alt: Outline of analysis for three different pixels.  
   
   Following values

**II. HOW TO USE**

First, open the 'user_config' text file in your 'Root_Processing' directory.  The parameters used in 'RP_mask' are in the 4th section, and there will be five parameters.  In order, they are:

1. image_filename: this is the full image filename (including directory) where the image is to be found.  

2. output_filename: this is the full image filename (including directory) where the image is to be saved.  If the directory is not present, the analysis will automatically make the directory.  

3. windowsize: this is the size of the window


3. b_w: scattering coefficient of water [cm^-2]

4. s_w: attenuation coefficient of water [cm^-2]

5. s_a: attenuation coefficient of aluminum [cm^-1]

6. s_s: attenuation coefficient of silicon [cm^-1]

7. x_s: thickness of soil [cm].  This is the thickness of the soil in the neutron beam direction.

8. x_a: thickness of aluminum [cm]. This is the thickness of the aluminum plates (in total, so both plates) in the neutron beam direction.

**III. RUNNING THE CODE**

This analysis can be conducted using the ['RP_wc'] string in the 'RP_run' module.  

---------------

.. [1] Kang, M et al., "Water calibration measurements for neutron radiography: Application to water content quantification in porous media." Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment 708 (2013):24-31.