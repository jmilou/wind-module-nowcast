import numpy as np
from modules.utils import bearing2rad, get_bearing, vector_from_polar
from geopy.distance import geodesic

site1_lat = -24.627135
site1_long = -70.404413
site2_lat = -24.589447
site2_long = -70.191790
bin_width = 2  # bin_width used for cross corr

site1_coord = np.array([site1_lat, site1_long])
site2_coord = np.array([site2_lat, site2_long])


phase_site1_site2 = bearing2rad(get_bearing(*site1_coord, *site2_coord))
d_abs = geodesic(site1_coord, site2_coord).km

d = vector_from_polar(d_abs, phase_site1_site2)
