import os
import glob
from tqdm import tqdm
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

ls_path = "/Volumes/LaCie/workfolder/sajag_nepal/susceptibility/Alex_nocoseismic_model/ls_vectors/Epoch04_FINAL_TopologyFixed.shp"
# polys_path = "/Volumes/LaCie/workfolder/sajag_nepal/susceptibility/Alex_nocoseismic_model/polygong_grids/polygongrid10000m.gpkg"

def get_count_of_landslide_in_grid(ls_path, polys):
    # copy GeoDataFrame and trasnform to points
    ls = gpd.read_file(ls_path)
    ls = ls[["id", "geometry"]]
    points = ls.copy()
    points['geometry'] = points['geometry'].centroid

    # Attach points to polygons
    # polys = gpd.read_file(polys_path)
    polys["fid"] = range(0, len(polys))
    pp_join = gpd.sjoin(polys, points) #Spatial join Points to polygons
    # pp_join.fillna(0, inplace=True)
    df = pp_join.groupby(['fid']).size().reset_index(name='counts')

    gdf = pd.merge(polys, df, on="fid", how="outer")
    gdf.fillna(0, inplace=True)

    # gdf.plot("counts", legend=True)
    # plt.show()

    return gdf