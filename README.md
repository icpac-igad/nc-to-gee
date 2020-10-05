# nc-to-gee

Upload Netcdf Files to GEE ImageCollection

- Convert NetCDF file to Geotiffs, based on time
- Create GEE metadata csv
- Upload to GEE ImageCollection using [geeup cli](https://github.com/samapriya/geeup)

```
geeup upload --source path/to/output/tiff --dest full/gee/path -u yourgee@email.com -m path/to/metadata.csv

```

