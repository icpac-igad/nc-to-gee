import xarray as xr
import rioxarray

variable = 'dailyrain'

ds = xr.open_dataset("PrecDaily.nc")

data_var = ds[variable]

data_var.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
data_var.rio.write_crs("epsg:4326", inplace=True)

data_var.rio.to_raster("PrecDaily.tif")
