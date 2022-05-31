import numpy as np
import pandas as pd
import geopandas as gpd

grid = ""
csize = 10000
numberbins = 100
rastevalue = 'AW3D_10m_Nepal_UTM45N_mask'
grid = grid[grid[rastevalue] >= 0]

grid.plot(grid.columns[1], c="Viridis", legend=True)


def bin_raster_and_create_frequency_ratios(grid, rastervalue, cellsize, numberbins):
    v = grid[grid.columns[1]].values
    bins = np.linspace(0, v.max(), num=numberbins)
    inds = np.digitize(v, bins, right=True)
    countperbin = np.bincount(inds)

    area = (csize / 1e3) ** 2  # km2

    df = pd.DataFrame({'binned_value': bins, 'total_area': [area*c for c in countperbin]})
    df["value"] = range(len(df))
    df["cumulative_binned_value"] = np.cumsum(df["total_area"])
    df["cumulative_binned_value_prec"] = df["cumulative_binned_value"] / df["cumulative_binned_value"].max()


    rastevalue = 'Landslide_presence_10m'
    ls_grid = grid[grid[rastevalue] == 1]

