import os
from os import listdir
from os.path import isfile, join

readPath = "data_sample/"
savePath = "data_sample/wgs84"
if not os.path.exists(savePath):
    os.makedirs(savePath)

onlyFiles = [f for f in listdir(readPath) if isfile(join(readPath, f))]

for fName in onlyFiles:
    dstnPath = os.path.join(savePath, 'WGS84_'+fName)
    os.system('gdalwarp %s %s -t_srs "+proj=longlat +ellps=WGS84"'
              % (readPath+fName, dstnPath))
