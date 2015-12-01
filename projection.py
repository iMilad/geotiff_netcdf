import os
from os import listdir
from os.path import isfile, join


# Convert to WGS84
def reprojection(filesPath):

    readPath = filesPath
    savePath = filesPath + "/wgs84"

    # Create folder if savePath doesn't exist
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # Collect all files tiff files and put them in a list
    onlyFiles = [f for f in listdir(readPath) if isfile(join(readPath, f))]

    # Convert each file into WGS84 with gdalwarp
    for fName in onlyFiles:
        dstnPath = os.path.join(savePath, 'WGS84_'+fName)
        os.system('gdalwarp %s %s -t_srs "+proj=longlat +ellps=WGS84"'
                  % (readPath+fName, dstnPath))
