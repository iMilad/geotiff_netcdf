"""
Created on Jan 13, 2015

Creating Color Table for matplotlib package

@author: Milad Khakpour,  milad.khakpour@gmail.com
"""

import os
from os.path import realpath, join


# Extract absolute image stack path
def extr_absimg_path(imgPath):

    """
    Parameters
    ----------
    imgPath: Path to imagestacks folder

    Returns
    -------
    Text file contains absolute image's path
    """

    for root, dirs, files in os.walk(imgPath):
        abs_img_txt = open('absolute_img_path.txt', 'w')
        for name in files:
            if name.endswith('.tif'):
                name = realpath(join(root, name))
                abs_img_txt.write(name + '\n')
        abs_img_txt.close()


def extr_img_path(imgPath):

    """
    Parameters
    ----------
    imgPath: Path to imagestacks folder

    Returns
    -------
    Text file contains absolute image's path
    """

    img_txt = open('img_path.txt', 'w')
    for paths, subdirs, files in os.walk(imgPath):
        for name in files:
            if name.endswith('.tif'):
                img_txt.write(join(paths, name) + '\n')
    img_txt.close()
