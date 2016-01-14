"""
Created on Jan 13, 2015

Creating Color Table for matplotlib package

@author: Milad Khakpour,  milad.khakpour@gmail.com
"""

import os
from os.path import realpath, join


# Extract image stack path
def extr_img_path(imgPath):

    """
    Parameters
    ----------
    imgPath: Path to imagestacks folder

    Returns
    -------
    Text file contains absolute image's path
    """

    for root, dirs, files in os.walk(imgPath):
        img_txt = open('absolute_img_path.txt', 'w')
        for name in files:
            if name.endswith('.tif'):
                name = realpath(join(root, name))
                print name
                img_txt.write(name + '\n')
        img_txt.close()
