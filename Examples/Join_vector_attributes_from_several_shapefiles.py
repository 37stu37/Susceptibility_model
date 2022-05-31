# %%
import geopandas as gpd
import os
import glob

# %%
datapath = "/Volumes/Nepal/SajagNepal/003_GIS_data/_TEMP/Connectivity/QGIS"

# %%
# Make a search criteria to select the shapefiles files
search_criteria = "*_mean_atslopeunits.shp"
query = os.path.join(datapath, search_criteria)
print(query)
shp_list = glob.glob(query)
print(shp_list)

# %%
test = gpd.read_file(shp_list[1])
test.iloc[:, -3:]

# %%
# Join table to landslide count
lsd = gpd.read_file(os.path.join(datapath, "lsdcentroid_in_slopeunits.shp"))
lsd[["su_ID", "lsd", "geometry"]]

for shpfile in shp_list:
    print(f"{shpfile} in process ....")
    shp = gpd.read_file(shpfile)

    shp = shp.iloc[:, -3:-1]
    lsd = lsd.merge(shp, on='su_ID')

    print(lsd.columns)


# %%
# Write lsd file to shape
lsd.to_file(os.path.join(datapath, "lsdcount_withrastersattributes.shp"))

# %%
# Remobe NAN rows and write to file
lsd_nonan = lsd.dropna()
lsd_nonan.to_file(os.path.join(datapath, "lsdcount_withrastersattributes_nonan.shp"))


