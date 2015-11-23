import os
from os import listdir
from os.path import isfile, join

myPath = "data_sample/"
onlyFiles = [f for f in listdir(myPath) if isfile(join(myPath, f))]

for fName in onlyFiles:
    os.system('gdalwarp %s %s -t_srs "+proj=longlat +ellps=WGS84"'
              % (myPath+fName, myPath+'WGS84_'+fName))
