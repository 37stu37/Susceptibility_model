import numpy as np
import pandas as pd
import geopandas as gpd

grid = ""
csize = 10000
numberbins = 100
rastename = 'AW3D_10m_Nepal_UTM45N_mask'

# grid.plot(grid.columns[1], c="Viridis", legend=True)


def bin_raster_and_create_frequency_ratios(grid, cellsize, numberbins):
    grid = grid[grid.iloc[:,1] >= 0]
    v = grid[grid.columns[1]].values
    bins = np.linspace(0, v.max(), num=numberbins)
    inds = np.digitize(v, bins, right=True)
    countperbin = np.bincount(inds)

    area = (cellsize / 1e3) ** 2  # km2

    df = pd.DataFrame({'binned_value': bins, 'total_area': [area*c for c in countperbin]})
    df["value"] = range(len(df))
    df["cumulative_binned_value"] = np.cumsum(df["total_area"])
    df["cumulative_binned_value_prec"] = df["cumulative_binned_value"] / df["cumulative_binned_value"].max()



    # Doing the same for landslide areas ONLY
    ls_grid = grid[grid.iloc[:, 2] == 0]

    v = ls_grid[ls_grid.columns[1]].values
    bins = np.linspace(0, v.max(), num=numberbins)
    inds = np.digitize(v, bins, right=True)
    countperbin = np.bincount(inds)

    area = (csize / 1e3) ** 2  # km2

    df_ls = pd.DataFrame({'binned_value': bins, 'total_area': [area * c for c in countperbin]})
    df_ls["value"] = range(len(df_ls))
    df_ls["cumulative_binned_value"] = np.cumsum(df_ls["total_area"])
    df_ls["cumulative_binned_value_prec"] = df_ls["cumulative_binned_value"] / df_ls["cumulative_binned_value"].max()


    # join the two
    df_join = df.merge(df_ls, on="binned_value", how="outer")

    return df_join
