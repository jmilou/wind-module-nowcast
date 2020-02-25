"""
This script takes care of making a dictionary filled with matrices that
help the latter visualization
"""
from modules.utils import bearing2rad, vector_from_polar
from modules.utils import get_diff_kinds, normalize
from modules.config import d, bin_width
import numpy as np
import pickle
from datetime import datetime, timedelta
from modules.open_files import wind, max_corr


wind.sort_values(['datetime', 'kind_of_data'], inplace=True)
height, winddirection, horizontalvelocity = get_diff_kinds(wind)

# making the phase of the wind vector
colsbearing2phase = [col for col in winddirection.columns if not('a' in col)]
tuple_col = tuple(colsbearing2phase)
bearing2rad_values = bearing2rad(winddirection[colsbearing2phase])


# velocities as vectors in two matrices
phase = bearing2rad_values.values
r = horizontalvelocity[colsbearing2phase].values
# the wind direction is from where it is blowing, that is why the minus sign is there
vel = -vector_from_polar(r, phase)
x_vel, y_vel = vel
# datetime as vector and height as matrix
date_time = winddirection['datetime'].values.reshape(-1)
UT_date_key = winddirection['date_key'].values.reshape(-1)
height_np = height[colsbearing2phase].values
# for all the matrices, the first index is the index corresponding to the timestamp and date_key

mod_vel = np.sqrt(x_vel**2 + y_vel**2)

#normalizing v
v_hat = normalize(vel)
ones = np.ones(vel.shape[1:])
#matrix with the distance
D = np.array([ones * d[0], ones * d[1]])
d_proyected = (D*v_hat).sum(axis=0)
time_predicted = 60 * d_proyected / mod_vel
UT_date_key = np.array([(datetime.strptime(i, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d') for i in UT_date_key.tolist()])



wind = dict(datetime=date_time,
            date_key=UT_date_key,
            height_wind=height_np,
            x_vel=x_vel,
            y_vel=y_vel,
            time_predicted=time_predicted,
            d_proyected=d_proyected,
            mod_vel=v_hat)


# passing the wind date_keys to UT
date_keys = max_corr['date_key'].unique().tolist()

df_2_get_max_corr = max_corr[max_corr['bin_width'] == bin_width]

dict_max_corr_lag = {}

# This makes a dictionary with all the lags in minutes of the correlations
for date in date_keys:
    condition1 = df_2_get_max_corr['date_key'] == date
    condition2 = df_2_get_max_corr[condition1]['cross_corr'] == df_2_get_max_corr[condition1]['cross_corr'].max()
    dict_max_corr_lag[date] = float(df_2_get_max_corr[condition1 & condition2].lag_in_minutes.values)


max_corr_4_wind_struct = []
for i in wind['date_key']:
    if i in date_keys:
        max_corr_4_wind_struct.append(dict_max_corr_lag[i])
    else:
        max_corr_4_wind_struct.append(np.nan)

shape = wind['time_predicted'].shape
wind['max_corr_lag'] = np.tile(np.array(max_corr_4_wind_struct), (shape[1],1)).T
wind['diff_time_lag'] = np.abs(wind['max_corr_lag'] - wind['time_predicted'])

# write file
with open('final_output/numpy_data.matrices', 'wb') as f:
    pickle.dump(wind, f)
f.close()
