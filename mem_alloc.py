import numpy as np
import datetime as dt
import os
import gdal
import netCDF4
import re
import datetime


def tiff_to_netcdf(imagesPath, output, chunksize=None):

    """
    Parameters
    ----------
    imagesPath : Path to image folder
    output : output name
    chunksize : chunk's size as tuple or list
                [time, lat, lon]

    Returns
    -------
    One nc file (NetCDF4 format) contains imagestacks
    """

    start = datetime.datetime.now()
    print '\nExecution started at: ', start, '\n'

    images = []
    for paths, subdirs, files in os.walk(imagesPath):
        for name in files:
            images.append(os.path.join(paths, name))

    ds = gdal.Open(images[0])

    a = ds.ReadAsArray()
    nlat, nlon = np.shape(a)

    b = ds.GetGeoTransform()  # bbox, interval
    lon = np.arange(nlon)*b[1]+b[0]
    lat = np.arange(nlat)*b[5]+b[3]

    basedate = dt.datetime(2006, 01, 11, 0, 0, 0)

    # Create NetCDF file
    # Clobber- Overwrite any existing file with the same name
    nco = netCDF4.Dataset(output+'.nc', 'w', clobber=True)

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
                              zlib=True, chunksizes=chunksize, fill_value=-9999)
    tmno.scale_factor = 0.01
    tmno.add_offset = 0.00
    tmno.grid_mapping = 'crs'
    tmno.set_auto_maskandscale(False)

    nco.Conventions = 'CF-1.6'

    # Write lon,lat
    lono[:] = lon
    lato[:] = lat

    pat = re.compile(r'^(\w{1})(\d{4})(\d{2})(\d{2})_\d{6}___SIG0.*.tif$')
    itime = 0
    written = 0
    data = np.empty((3, 8000, 8000), dtype=np.float)

    # Step through data, writing time and data to NetCDF
    for root, dirs, files in os.walk(imagesPath):
        dirs.sort()
        files.sort()
        for f in files:

            match = re.match(pat, f)
            if match:

                if itime  % 3 == 0 and itime != 0:
                    tmno[written:itime, :, :] = data
                    written = itime
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
                data[itime%3, :, :] = a
                itime = itime+1


    nco.close()

    stop = datetime.datetime.now()
    print '\nExecution Ended at: ', stop, '\nElapsed time: ', stop - start
