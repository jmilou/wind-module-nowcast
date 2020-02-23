"""
This file has all the functions that may be needed for the project
to work properly
"""
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import math

def grouper_UT(df, UTb, UTe):
    '''
    df: df to slice (must be sorted by date)
    UTb: begining UT time of interest
    UTe: end of UT time of interest (next day)

    return: a list of dfs with the slices
    '''
    datetime_vals = pd.to_datetime(df.datetime.values)

    n_days = (datetime_vals[-1] - datetime_vals[0]).days

    date_0 = datetime_vals.date[0]
    date_f = date_0 + timedelta(days=1)

    date_0 = datetime.combine(date_0, UTb)
    date_f = datetime.combine(date_f, UTe)

    condition = (date_0 < datetime_vals) & (datetime_vals < date_f)
    conditions = [condition]
    conditions += [((date_0 + timedelta(days=i)) < datetime_vals) & (
            datetime_vals < (date_f + timedelta(days=i)))
                   for i in range(n_days)]

    UT_days = [df.loc[single_condition] for single_condition in conditions]

    return UT_days


def list2dict(list_dfs):
    """
    it takes a list of sliced dfs and turns it into a dict with
    the date as key
    :param list_dfs: a list of ut sampled dfs
    :return: a dict of ut sampled dfs
    """

    return {pd.to_datetime(df.datetime.values)[0].strftime('%Y-%m-%d'): df for
            df in list_dfs}


def bearing2rad(angle_bearing):
    """
    this function takes a bearing angle and transforms it into an angle
    in polar coordinates
    :param angle_bearing: angle to transform
    :return: angle for polar coord
    """
    return np.pi/2 - angle_bearing * np.pi / 180


def get_bearing(lat1, lon1, lat2, lon2):
    """
    it returns the bearing anle between two coordinates
    credits to: https://stackoverflow.com/users/1019167/alexwien
    :return: bearing in degrees
    """
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * \
        math.cos(lat2) * math.cos(dLon)
    brng = np.rad2deg(math.atan2(y, x))
    if brng < 0:
        brng += 360
    return brng


def find_angle_of_vector(vector):
    """
    returns the angle of the vector in radians
    :param vector: vector for which to search the angle
    :return: angle in radians
    """
    x, y = vector
    tan = y / x
    return np.arctan(tan)



def find_base():
    pass

def find_max_lag_neg_or_pos():
    pass





def proyect_velocity(velocity):
    """
    proyects the velocity vector in a vertical and horizontal velocity
    :param velocity: vector velocity in rec coord
    :return: vertical velocity proyection, horixontal velocity
    """
    pass

def filter_df_by_date_key(df, date_key):
    """
    takes a df and retuns a df by the date key

    :param df: df to filter
    :param date_key: date key to filter by
    :return: filtered df
    """

    return df[df['date_key'] == date_key]


def get_diff_kinds(df):
    """
    this function takes the wind dataframe data and split it into three
    dfs for the data of the different kinds

    :param df: wind data df
    :return: 3 dfs of that day but splitted by kind of data
    """

    h_filter = df['kind_of_data'] == 'height'
    w_d_filter = df['kind_of_data'] == 'winddirection'
    h_v_filter = df['kind_of_data'] == 'horizontalvelocity'

    height = df[h_filter]
    winddirection = df[w_d_filter]
    horizontalvelocity = df[h_v_filter]

    return height, winddirection, horizontalvelocity




def vector_from_polar(r, theta):
    return np.array([r * np.cos(theta), r * np.sin(theta)])


def normalize(v):
    return v / (np.sqrt(np.square(v[0, :, :]) + np.square(v[1, :, :])))




