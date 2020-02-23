"""
This file takes all the wind data and it outputs a binary dataframe
"""
import pandas as pd
import os
import pickle
from datetime import time
from modules.utils import grouper_UT, list2dict
UT_interval = time(22, 0, 0), time(11, 0, 0)

# gathering paths for the csvs
files_paths = [i for i in os.listdir('files2reformat') if ('.csv' in i)]
files_paths.sort()

# making dictionary of dataframes from the files
dfs_dict = {}
for file_path in files_paths:
    name = file_path[:-4]
    dfs_dict[name] = pd.read_csv('./files2reformat/' + file_path)
    dfs_dict[name].rename(columns={"Unnamed: 0": "datetime"}, inplace=True)
    dfs_dict[name]['datetime'] = pd.to_datetime(dfs_dict[name]['datetime'])
    numcol = [i for i in dfs_dict[name].columns if i != 'datetime']
    for col in numcol:
        dfs_dict[name][col] = pd.to_numeric(dfs_dict[name][col],
                                            errors='coerce')

# making different list for different kid of csv
Height_vs_pressure_list_df = [dfs_dict[key] for key in dfs_dict if ('Height_vs_pressure' in key)]
Horizontalvelocity_vs_pressure_list_df = [dfs_dict[key] for key in dfs_dict if ('Horizontalvelocity_vs_pressure' in key)]
Winddirection_vs_pressure_list_df = [dfs_dict[key] for key in dfs_dict if ('Winddirection_vs_pressure' in key)]

# merging each list into a different df
Height_vs_pressure_df = pd.concat(Height_vs_pressure_list_df)
Horizontalvelocity_vs_pressure_df = pd.concat(Horizontalvelocity_vs_pressure_list_df)
Winddirection_vs_pressure_df = pd.concat(Winddirection_vs_pressure_list_df)

# drop nans
Height_vs_pressure_df.dropna(thresh=2, inplace=True)
Horizontalvelocity_vs_pressure_df.dropna(thresh=2, inplace=True)
Winddirection_vs_pressure_df.dropna(thresh=2, inplace=True)

# creating 'kind_of_data' columns
Height_vs_pressure_df['kind_of_data'] = 'height'
Horizontalvelocity_vs_pressure_df['kind_of_data'] = 'horizontalvelocity'
Winddirection_vs_pressure_df['kind_of_data'] = 'winddirection'

df = pd.concat([Height_vs_pressure_df, Horizontalvelocity_vs_pressure_df, Winddirection_vs_pressure_df])
df.sort_values('datetime', inplace=True)
df.reset_index(inplace=True)

# date_key columns
df = df[[i for i in df.columns if i != 'index']]

# now taking care of UT time
UT_sliced = grouper_UT(df, *UT_interval)
dict_UT = list2dict(UT_sliced)

dfs4concat = []
for date_key in dict_UT:
    current_df = dict_UT[date_key]
    current_df.loc[:, ('date_key')] = date_key
    dfs4concat.append(current_df)

final_df = pd.concat(dfs4concat)

# saving the new df
with open('final_output/wind_data.df', 'wb') as f:
    pickle.dump(final_df, f)
f.close()
