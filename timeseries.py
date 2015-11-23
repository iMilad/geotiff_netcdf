import numpy as np
import datetime as dt
import os
import gdal
import netCDF4
import re

import time

start = time.strftime("%c")
print start

ds = gdal.Open('data_sample/R20060111_075725___SIG0__ASAWS___M1VVD_TUW_SGRT15A00_AF075M_E060N054T6.tif')

a = ds.ReadAsArray()
nlat, nlon = np.shape(a)

b = ds.GetGeoTransform()  # bbox, interval
lon = np.arange(nlon)*b[1]+b[0]
lat = np.arange(nlat)*b[5]+b[3]

basedate = dt.datetime(2006, 01, 11, 0, 0, 0)

# Create NetCDF file
# Clobber- Overwrite any existing file with the same name
nco = netCDF4.Dataset('time_series.nc', 'w', clobber=True)

# chunk_lon = 16
# chunk_lat = 16
# chunk_time = 50

# Create dimensions, variables and attributes:
nco.createDimension('lon', nlon)
nco.createDimension('lat', nlat)
nco.createDimension('time', None)

timeo = nco.createVariable('time', 'f4', ('time',))
timeo.units = 'days since 2006-01-11 00:00:00'
timeo.standard_name = 'time'

lono = nco.createVariable('lon', 'f4', ('lon',))
lono.standard_name = 'longitude'

lato = nco.createVariable('lat', 'f4', ('lat',))
lato.standard_name = 'latitude'

# Create container variable for CRS: lon/lat WGS84 datum
crso = nco.createVariable('crs', 'i4')
crso.long_name = 'Lon/Lat Coords in WGS84'
crso.grid_mapping_name = 'latitude_longitude'
crso.longitude_of_prime_meridian = 0.0
crso.semi_major_axis = 6378137.0
crso.inverse_flattening = 298.257223563

# Create short integer variable with chunking
tmno = nco.createVariable('tmn', 'i2',  ('time', 'lat', 'lon'),
                          zlib=True, fill_value=-9999)
tmno.scale_factor = 0.01
tmno.add_offset = 0.00
tmno.grid_mapping = 'crs'
tmno.set_auto_maskandscale(False)

nco.Conventions = 'CF-1.6'

# Write lon,lat
lono[:] = lon
lato[:] = lat

pat = re.compile(r'^(\w{1})(\d{4})(\d{2})(\d{2})_\d{6}')
itime = 0

# Step through data, writing time and data to NetCDF
for root, dirs, files in os.walk('/media/sf_R/Datapool_processed'
                                 + '/Envisat_ASAR/WS/preprocessed/SGRT15A00'
                                 + '/datasets/resampled/EQUI7_AF075M'
                                 + '/E060N054T6'):
# for root, dirs, files in os.walk('data_sample'):
    dirs.sort()
    files.sort()
    for f in files:
        match = re.match(pat, f)
        if match:
            # read the time values by parsing the filename
            year = int(match.group(2))
            mon = int(match.group(3))
            day = int(match.group(4))
            date = dt.datetime(year, mon, day, 0, 0, 0)
            print(date)
            dtime = (date-basedate).total_seconds()/86400.
            timeo[itime] = dtime
            tmn_path = os.path.join(root, f)
            print(tmn_path)
            tmn = gdal.Open(tmn_path)
            a = tmn.ReadAsArray()  # data
            tmno[itime, :, :] = a
            itime = itime+1

nco.close()

stop = time.strftime("%c")

print start
print stop
