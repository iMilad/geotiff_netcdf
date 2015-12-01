import os


# Convert to WGS84
def reprojection(filesPath):

    readPath = filesPath
    savePath = filesPath + "/wgs84"

    # Create folder if savePath doesn't exist
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # Collect all tiff files and put them in a list
    tiffs = []
    for f in os.listdir(readPath):
        if f.endswith(".tif"):
            tiffs.append(f)

    # Convert each file into WGS84 with gdalwarp
    for fName in tiffs:
        dstnPath = os.path.join(savePath, 'WGS84_'+fName)
        os.system('gdalwarp %s %s -t_srs "+proj=longlat +ellps=WGS84"'
                  % (readPath+fName, dstnPath))
