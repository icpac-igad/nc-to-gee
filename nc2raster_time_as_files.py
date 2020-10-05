import xarray as xr
import rioxarray

variable = 'dailyrain'
output_dir = "output/tiff"

ds = xr.open_dataset("~/Downloads/Data/ICPAC/FORECAST/WEEKLY/20200825/PrecDaily.nc")

prefix = "WR"  # for Weekly Rainfall Forecast

for idx, time in enumerate(ds.time):
    time = time.values
    timestamp = time.astype('datetime64[s]').astype('int')
    ds_sel = ds.isel(time=idx)

    data_var = ds_sel[variable]
    data_var.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
    data_var.rio.write_crs("epsg:4326", inplace=True)

    data_var.rio.to_raster(f"{output_dir}/{prefix}{timestamp}.tif")
