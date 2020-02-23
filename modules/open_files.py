import pickle

with open('correlation_df_file/max_corr_df.correlations', 'rb') as f:
    max_corr = pickle.load(f)
f.close()

max_corr.reset_index(drop=True, inplace=True)

with open('final_output/wind_data.df', 'rb') as f:
    wind = pickle.load(f)
f.close()
