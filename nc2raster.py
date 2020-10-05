import gdal, gdalconst, osr
import numpy
from netCDF4 import Dataset

# Open the NetCDF file for reading.
fh = Dataset(r"PrecDaily.nc", "r")

# Read your parameter into a numpy array.
# Depending on your dataset you may have to specify additional index values
# e.g. Time.
values = numpy.array(fh.variables["f90"])
value2 = numpy.array(fh.variables["f95"])
value3 = numpy.array(fh.variables["f99"])

# Now you can manipulate your array.
"""
perform calculations in the array
"""
lon = numpy.array(fh.variables["lon"])
lat = numpy.array(fh.variables["lat"])
top_left_x = lon.item(0)
top_left_y = lat.item(len(lat) - 1)
x_step = (lon.max() - lon.min()) / len(lon)
y_step = (lat.max() - lat.min()) / len(lat)
rotation = 0

# Get array dimensions so we can create an equal size tiff file.
rows, cols = values.shape

# Create output tiff file.
# driver.Create() parameters are: output path, number of columns, number of rows,
# number of bands, data type
driver = gdal.GetDriverByName("GTiff")
out_data = r"precExtreme.tiff"
out_tif = driver.Create(out_data, cols, rows, 3, gdalconst.GDT_Float32)

# Create Spatial Reference object and set GeoTIFF projection.
# This information may be found in either the data documentation or the netCDF file.
prj = osr.SpatialReference()
prj.ImportFromEPSG(4326)  # WGS84
out_tif.SetProjection(prj.ExportToWkt())

# Set GeoTransformation.
# This information may be found in either the data documentation, the netCDF file, or
# can be derived. For example, if you know the longitude range and number of columns
# you can calculate the x step as float(lon_range)/float(num_cols).
geotrans = [top_left_x, x_step, rotation, top_left_y, rotation, y_step]
out_tif.SetGeoTransform(geotrans)

# Finally we can write the array to the raster band.
out_band = out_tif.GetRasterBand(1)
out_band.WriteArray(values)
out_band = out_tif.GetRasterBand(2)
out_band.WriteArray(value2)
out_band = out_tif.GetRasterBand(3)
out_band.WriteArray(value3)

# Clear the memory and close the output file.
out_tif.FlushCache()
out_tif = None
