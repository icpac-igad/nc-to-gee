from osgeo import gdal
import pandas as pd
import os

in_dir = 'output/tiff'
out_csv = "output/metadata.csv"

meta_keys = ['longname', 'units']

csv_keys = ['id_no', 'system:time_start']
csv_keys.extend(meta_keys)

df = pd.DataFrame(columns=csv_keys)

for root, dirs, files in os.walk(in_dir):
    for file in files:
        if file.endswith(".tif"):
            path = os.path.join(root, file)  # make path
            raster = gdal.Open(path, gdal.GA_ReadOnly)  # Open Raster in GDAL
            meta = dict.fromkeys(csv_keys)  # Make a dict to store key, values

            # Get time from filename
            timestamp_str = file[2:-4]

            meta['id_no'] = os.path.splitext(file)[0]
            meta['system:time_start'] = int(timestamp_str)

            for key in meta_keys:
                meta[key] = raster.GetMetadataItem(key)

            df = df.append(meta, ignore_index=True)

df.to_csv(out_csv, index=False)
