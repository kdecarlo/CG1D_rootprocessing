.. tutorial_rootdiameter:

*******************************
Getting Started: rootdiameter
*******************************

**I. OVERVIEW**

The 'RP_rootdiameter' analysis creates a text file of the root diameter distribution using the root mask image.  The user has an option to bin the root diameter values, and all results are shown in terms of pixels.

**II. HOW TO USE**

First, open the 'user_config' text file in your 'Root_Processing' directory.  The parameters used in 'rootdiameter' are in the 9th section, and there will be three parameters.  In order, they are:

1. mask_filename: this is the full image filename (including directory) where the mask image is to be found. 

2. output_filename: this is the full image filename (including directory) where the outputted files will be saved.

3. bincount: the number of bins the root diameter is to be placed into.

**III. RUNNING THE CODE**

This analysis can be conducted using the ['RP_rootdiameter'] string in the 'RP_run' module.  