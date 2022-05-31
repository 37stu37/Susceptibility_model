import numpy as np

grid = ""
numberbins = 100
rastevalue = 'AW3D_10m_Nepal_UTM45N_mask'
v = grid[grid[rastevalue] >=0].values

bins = np.linspace(0, v.max(), num=numberbins)
inds = np.digitize(v, bins, right=True)
countperbin = np.bincount(inds)

