import os
import glob
from tqdm import tqdm
import geopandas as gpd
import rasterio as rio

path_to_rasterlist = ""


def raster_value_at_polygon_grid(polygongrid, path_to_rasterlist, search_criteria, output_path, cellsize):
    # Make a search criteria to select the raster files
    search_criteria = search_criteria
    q = os.path.join(path_to_rasterlist, search_criteria)
    rasterlist = glob.glob(q)
    print(rasterlist)

    print(" ")
    print(" ")
    print("Starting rasters value extraction...")

    # Extract raster values for each polygon centroids
    for r in rasterlist:
        coords = [(x, y) for x, y in zip(polygongrid.centroid.x, polygongrid.centroid.y)]
        print(" ")
        print(" ")
        print(f'{r.split("/")[-1][:-4]}')
        print(f"number of coordinates to extract : {len(coords)}")
        raster = rio.open(r)
        rastervalues = [x[0] for x in tqdm(raster.sample(coords))]
        polygongrid[f'{r.split("/")[-1][:-4]}'] = rastervalues

    # polygongrid.to_file(os.path.join(output_path, f"polygongrid_wrastervalues_{cellsize}m.gpkg"), driver="GPKG")

    print(" ")
    print(" ")
    print(f"polygongrid_wrastervalues_{cellsize}m created")

    return polygongrid
