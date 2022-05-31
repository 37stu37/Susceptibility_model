from Create_regular_polygon_grid import *
from Spatial_join_and_count_pts_in_polygon import *
from Extract_raster_value_per_polygon_centroid import *

# Variables
hdr_path = "/Volumes/LaCie/workfolder/sajag_nepal/susceptibility/Alex_nocoseismic_model/"
ls_path = "/Volumes/LaCie/workfolder/sajag_nepal/susceptibility/Alex_nocoseismic_model/ls_vectors/Epoch04_FINAL_TopologyFixed.shp"
extent_raster_path = os.path.join(hdr_path, "10m_rasters", "AW3D_10m_Nepal_UTM45N_mask.tif")
to_rasters_list = os.path.join(hdr_path, "10m_rasters")

s_criteria = "*mask.tif"
cell_size = 1000
out_path = os.path.join(hdr_path, "polygong_grids")
CRS = 32645

g = create_polygon_grid(cell_size, extent_raster_path, out_path, CRS)
gdf = get_count_of_landslide_in_grid(ls_path, g)
grid_rasters = raster_value_at_polygon_grid(gdf, to_rasters_list, s_criteria, out_path, cell_size)

print(" ")
print(" ")
print("------ END ------")