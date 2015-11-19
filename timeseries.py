import numpy as np
import datetime as dt
import os
import gdal
import netCDF4
import re

ds = gdal.Open('/home/pydev/Desktop/2015/sar_tasks/task2_GeoTIFF_to_NetCDF/data_sample/R20060111_075725___SIG0__ASAWS___M1VVD_TUW_SGRT15A00_AF075M_E060N054T6.tif')

a = ds.ReadAsArray()
nlat, nlon = np.shape(a)

b = ds.GetGeoTransform()  # bbox, interval
lon = np.arange(nlon)*b[1]+b[0]
lat = np.arange(nlat)*b[5]+b[3]

basedate = dt.datetime(2006, 01, 11, 0, 0, 0)

# Create NetCDF file
# Clobber- Overwrite any existing file with the same name
nco = netCDF4.Dataset('time_series.nc', 'w', clobber=True)

chunk_lon = 16
chunk_lat = 16
chunk_time = 12

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

# Create short integer variable for temperature data, with chunking
tmno = nco.createVariable('tmn', 'i2',  ('time', 'lat', 'lon'),
                          zlib=True, chunksizes=[chunk_time,
                                                 chunk_lat,
                                                 chunk_lon],
                          fill_value=-9999)
tmno.units = 'degC'
tmno.scale_factor = 0.01
tmno.add_offset = 0.00
tmno.long_name = 'minimum monthly temperature'
tmno.standard_name = 'air_temperature'
tmno.grid_mapping = 'crs'
tmno.set_auto_maskandscale(False)

nco.Conventions = 'CF-1.6'

# Write lon,lat
lono[:] = lon
lato[:] = lat

# pat = re.compile('us_tmin_[0-9]{4}\.[0-9]{2}')
pat = re.compile('(\w{1})(\d{4})(\d{2})(\d{2})_\d{6}')
# pat = re.compile('us_(\w{1})(\d{4})(\d{2})(\d{2})')
itime = 0

# Step through data, writing time and data to NetCDF
for root, dirs, files in os.walk('/data_sample/'):
    dirs.sort()
    files.sort()
    for f in files:
        if re.match(pat, f):
            # read the time values by parsing the filename
            year = int(f[4:8])
            mon = int(f[8:10])
            date = dt.datetime(year, mon, 1, 0, 0, 0)
            print(date)
            dtime = (date-basedate).total_seconds()/86400.
            timeo[itime] = dtime
            # min temp
            tmn_path = os.path.join(root, f)
            print(tmn_path)
            tmn = gdal.Open(tmn_path)
            a = tmn.ReadAsArray()  # data
            tmno[itime, :, :] = a
            itime = itime+1

nco.close()
