import glob
import os

import geopandas as gpd
import numpy as np
import rasterio as rio
from shapely.geometry import Point
from shapely.geometry import box
from tqdm import tqdm

from B_Bin_raster import *

p = "/Volumes/LaCie/workfolder/sajag_nepal/susceptibility/Alex_nocoseismic_model/10m_rasters"
crs = 32645
csize = 10
s_criteria = "AW3D_10m_Nepal_UTM45N_mask*"


def raster_value_at_polygon_grid(path_to_rasters, search_criteria, cellsize, CRS):
    # Make a search criteria to select the raster files
    r_search = os.path.join(path_to_rasters, search_criteria)
    # Need the landslide presence raster
    ls_search = os.path.join(path_to_rasters, 'Landslide_presence_10m*')

    rasterlist = [glob.glob(q) for q in [r_search, ls_search]]
    rasterlist = [item for sublist in rasterlist for item in sublist] # need to flatten the list

    print(rasterlist[0])

    ra = rio.open(rasterlist[0])
    bounds = ra.bounds

    # Convert bounds to shapely geometry
    geom = box(*bounds)  # print(geom.wkt)
    rasterbox = gpd.GeoDataFrame({"id": 1, "geometry": [geom]})

    # Get the boundaries of the raster envelope
    xmin, ymin, xmax, ymax = rasterbox.total_bounds

    # Polygon sizes
    length = cellsize
    wide = cellsize

    cols = list(np.arange(xmin, xmax + wide, wide))
    rows = list(np.arange(ymin, ymax + length, length))

    print(f"Creating gridded points {length}m x {wide}m...")

    points = []
    for x in tqdm(cols[:-1]):
        for y in rows[:-1]:
            points.append(Point(x, y))

    grid = gpd.GeoDataFrame({'geometry': points})
    grid.set_crs(epsg=CRS, inplace=True)

    print(" ")
    print(" ")
    print("Starting rasters value extraction...")

    # Extract raster values for each points
    for r in rasterlist:
        coords = [(x, y) for x, y in zip(grid.centroid.x, grid.centroid.y)]
        print(" ")
        print(" ")
        print(f'{r.split("/")[-1][:-4]}')
        print(f"number of coordinates to extract : {len(coords)}")
        raster = rio.open(r)
        rastervalues = [x[0] for x in tqdm(raster.sample(coords))]
        grid[f'{r.split("/")[-1][:-4]}'] = rastervalues

    # grid.to_file(os.path.join(output_path, f"grid_wrastervalues_{cellsize}m.gpkg"), driver="GPKG")

    print(" ")
    print(" ")
    print(f"grid with raster values {cellsize}m created")

    return grid

grid = raster_value_at_polygon_grid(p, s_criteria, csize, crs)