import geopandas as gpd
import rasterio as rio
from shapely.geometry import Polygon
from shapely.geometry import box
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import glob

extent_rasterpath = ""
output_path = ""

def create_polygon_grid(cellsize, extent_rasterpath, output_path, grid_crs_epsg):
    # Create regular polygon grid
    # Get DEM total_bounds
    ra = rio.open(extent_rasterpath)
    bounds = ra.bounds

    # Convert bounds to shapely geometry
    geom = box(*bounds)  # print(geom.wkt)
    rasterbox = gpd.GeoDataFrame({"id": 1, "geometry": [box(*bounds)]})

    # Get the boundaries of the raster envelope
    xmin, ymin, xmax, ymax = rasterbox.total_bounds

    # Polygon sizes
    length = cellsize
    wide = cellsize

    cols = list(np.arange(xmin, xmax + wide, wide))
    rows = list(np.arange(ymin, ymax + length, length))

    print(f"Creating gridded polygon {length}m x {wide}m...")

    polygons = []
    for x in tqdm(cols[:-1]):
        for y in rows[:-1]:
            polygons.append(Polygon([(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]))

    grid = gpd.GeoDataFrame({'geometry': polygons})
    grid.set_crs(epsg=grid_crs_epsg, inplace=True)
    # grid.to_file(os.path.join(output_path, f"polygongrid{length}m.gpkg"), driver="GPKG")
    #
    # print(f"polygongrid{length}m created")

    return grid
