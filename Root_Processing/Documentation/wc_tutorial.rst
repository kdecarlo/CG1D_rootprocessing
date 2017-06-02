.. wc_tutorial:

************************
Getting Started: wc
************************

**I. OVERVIEW**

The 'RP_wc' analysis creates a water thickness map from the specified image using equations outlined in Kang et al., 2013 [1]_.  This analysis assumes that the images are in a quasi-2D (i.e. thin plate) form, with soil held together by two aluminum plates.  

Volumetric water content is defined as :math:`\theta = \\frac{V_w}{V_w_e_t}`

Output image must be a neutron transmission image, and the output image will show the thickness of water present in each pixel.


; multiplying the pixel value by the pixel area will get you the volume of water per pixel.  Dividing this by the pixel volume 

therefore, in order to calculate water content, one will need to multiply

**II. HOW TO USE**

First, open the 'user_config' text file in your 'Root_Processing' directory.  The parameters used in 'RP_crop' are in the 3rdd section, and there will be eight parameters.  In order, they are:

1. image_filename: this is the full image filename (including directory) where the image is to be found.  

2. output_filename: this is the full image filename (including directory) where the image is to be saved.  If the directory is not present, the analysis will automatically make the directory.  

3. b_w: scattering coefficient of water [cm^-2]

4. s_w: attenuation coefficient of water [cm^-2]

5. s_a: attenuation coefficient of aluminum [cm^-1]

6. s_s: attenuation coefficient of silicon [cm^-1]

7. x_s: thickness of soil [cm].  This is the thickness of the soil in the neutron beam direction.

8. x_a: thickness of aluminum [cm]. This is the thickness of the aluminum plates (in total, so both plates) in the neutron beam direction.

**III. RUNNING THE CODE**

This analysis can be conducted using the ['RP_crop'] string in the 'RP_run' module.  

---------------

.. [1] Kang, M et al., "Water calibration measurements for neutron radiography: Application to water content quantification in porous media." Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment 708 (2013):24-31.