from typing import List, Any, Tuple
from datetime import datetime
from sklearn import preprocessing
import pandas as pd
import streamlit as st


def hash_reference(_service):
    return hex(id(_service))


def hash_list_str(l: List[str]):
    res = hex(0)
    for x in l:
        res += hex(id(x))
    return res


@st.cache(hash_funcs={pd.DataFrame: hash_reference})
def clean_df(df: pd.DataFrame) -> pd.DataFrame:

    cols = df.columns
    # remove redundant column
    df.drop(cols[-1], inplace=True, axis=1)
    label_col = cols[-2]
    # give new label 2 to unlabeled data
    first_valid_position = df[label_col].index.get_loc(df[label_col].first_valid_index())
    df[label_col].fillna(2, limit=first_valid_position, inplace=True)
    # fill holes with 0 and remove duplicates
    df.fillna(0, inplace=True)
    df.drop_duplicates(inplace=True)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df


@st.cache(hash_funcs={pd.DataFrame: hash_reference})
def get_time_range(df: pd.DataFrame) -> Tuple[datetime, datetime]:
    start_time = df['datetime'].min()
    end_time = df['datetime'].max()
    return start_time, end_time


# @st.cache(hash_funcs={pd.DataFrame: hash_reference})
def get_labels(df: pd.DataFrame) -> List[str]:
    labels = df[df.columns[-1]].unique()
    return list(labels)


# @st.cache(hash_funcs={pd.DataFrame: hash_reference})
def get_channels(df: pd.DataFrame) -> List[str]:
    return ['Accelerometer1RMS', 'Accelerometer2RMS', 'Current', 'Pressure', 'Temperature',
            'Thermocouple', 'Voltage', 'Volume Flow RateRMS', ]
    return list(df.columns[1: -1])


# @st.cache(hash_funcs={pd.DataFrame: hash_reference, List[str]: hash_list_str})
def get_corr(df: pd.DataFrame, channels: List[str]):
    return df[channels].corr()


@st.cache(hash_funcs={pd.DataFrame: hash_reference})
def prepare_for_distribution_per_channel(df: pd.DataFrame) -> pd.DataFrame:
    channels = get_channels(df)
    scaled_df = df[channels]
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
    min_max_scaler.fit(scaled_df)
    scaled_df = min_max_scaler.fit_transform(scaled_df)
    scaled_df = pd.DataFrame(scaled_df, columns=channels)
    # scaled_df[df.columns[-1]] = df[df.columns[-1]]
    labels = df[df.columns[-1]]
    # channels = list(scaled_df.columns)
    result = pd.DataFrame(columns=['channel', 'value', 'label'])
    for channel in channels:
        temp = pd.DataFrame(columns=['channel', 'value', 'label'])
        temp['value'] = scaled_df[channel]
        temp['label'] = labels
        temp['channel'] = channel
        result = result.append(temp)

    return result


@st.cache(hash_funcs={pd.DataFrame: hash_reference})
def prepare_for_channel_correlation(df: pd.DataFrame, channels: List[str]) -> pd.DataFrame:
    columns = ['time'] + channels + ['label']
    labels = df[df.columns[-1]]
    times = df['datetime']
    result = pd.DataFrame(columns=columns)
    result['time'] = times
    result['label'] = labels
    for channel in channels:
        result[channel] = df[channel]

    return result
