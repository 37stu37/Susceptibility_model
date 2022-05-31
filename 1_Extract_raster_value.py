import geopandas as gpd
import rasterio as rio
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import box
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import glob

p = "/Volumes/LaCie/workfolder/sajag_nepal/susceptibility/Alex_nocoseismic_model/10m_rasters"
crs = 32645
csize = 10000


def raster_value_at_polygon_grid(path_to_rasterlist, search_criteria, cellsize, CRS):
    # Make a search criteria to select the raster files
    search_criteria = search_criteria
    q = os.path.join(path_to_rasterlist, search_criteria)
    rasterlist = glob.glob(q)
    print(rasterlist)

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
