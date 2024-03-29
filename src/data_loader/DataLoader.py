# import logging
import os
import xml.etree.ElementTree as ET
import regex as re
from tqdm.contrib.telegram import tqdm
import pandas as pd
from src.utils.Util import *
from src.utils.Delpher import Delpher

from src.utils.Settings import *
from src.data_loader.DBNL import *
from src.data_loader.Impact import *
from src.data_loader.Historical_newspaper import *
from src.data_loader.SeventeenthCentury import *
from src.data_loader.Statenvertaling import *

MIN_WORDS = 5
MAX_WORDS = 50
# READ_FROM_FILE = False


# BASE_PATH = '../../data/Ground Truth/'
# SAVE_FILE_PATH = BASE_PATH + "dataframes/target_year"

delpher = Delpher()
##### Utils

def clean_dataframe(df):
    if 'source' in df.columns:
        df['source'] = df['source'].apply(lambda x: str(x))
        df = df[df['source'].apply(lambda x: x != 'NaN' and x != None and x != 'None' and x != 'nan')]
        df = df.reset_index(drop=True)
        df = df[df['source'].apply(lambda x: len(x) > 1)]
    df['year'] = df['year'].apply(lambda x: str(x))
    df['target'] = df['target'].apply(lambda x: str(x))
    df['target'] = df['target'].replace(r'\s+', ' ', regex=True)
    df['target'] = df['target'].apply(lambda x: re.sub('[^A-Za-z0-9,.;\s]+', '', x))
    df['target'] = df['target'].apply(lambda x: x.strip())


    df = df[df['target'].apply(lambda x: x.count(' ') > MIN_WORDS and x.count(' ') < MAX_WORDS)]
    df = df[df['target'].apply(lambda x: len(x) > 0)]
    df = df[df['target'].apply(lambda x: not(any(char.isdigit() for char in x)))]
    df = df[df['target'].apply(lambda x: x != 'NaN' and x != None and x != 'None')]
    df = df[df['year'].apply(lambda x: x != '0000' and not '-' in str(x) and str(x) != '0')]
    df = df.drop_duplicates(subset=['target'])
    df = df.reset_index(drop=True)
    return df

def get_data():
    if os.path.exists(SAVE_PATH_PRE_OCR_CLEANED) and READ_FROM_FILE_PRE_OCR:
        df = read_pandas(SAVE_PATH_PRE_OCR_CLEANED)
        return df
    impact_newspapers = Impact(SAVE_PATH_IMPACT, 'Newspapers')
    impact_books = Impact(SAVE_PATH_IMPACT, 'Books')
    impact_parliamentary_proceedings = Impact(SAVE_PATH_IMPACT, 'Parliamentary Proceedings')
    impact_radiobulletins = Impact(SAVE_PATH_IMPACT, 'Radio Bulletins')
    dbnl = DBNL(SAVE_PATH_DBNL_BOOKS)
    historical_newspaper = HistoricalNewspaper(SAVE_PATH_HISTORICALNEWSPAPERS, delpher)
    seventeenth_century_newspaper = SeventeenthCentury(SAVE_PATH_17THCENTURYNEWSPAPER, delpher)
    statenvertaling = Statenvertaling(SAVE_PATH_STATENVERTALING)

    data_list = [impact_newspapers, impact_books, impact_parliamentary_proceedings, impact_radiobulletins, dbnl, historical_newspaper, seventeenth_century_newspaper, statenvertaling]
    # data_list = [impact_newspapers, impact_books, impact_parliamentary_proceedings, impact_radiobulletins, dbnl]
    # data_list = [impact_newspapers]
    # data_list = [statenvertaling]
    # data_list = [dbnl]
    # data_list = [seventeenth_century_newspaper]
    # data_list = [historical_newspaper]
    # data_list = [statenvertaling]
    # data_list = [impact_newspapers, impact_books, impact_parliamentary_proceedings, impact_radiobulletins]
    dataframes = []

    for item in data_list:
        temp_df = item.get_data()
        dataframes.append(temp_df)
        print(temp_df.head())
        print(temp_df.columns)

    df = pd.concat(dataframes)
    df = df.reset_index(drop=True)

    if WRITE_FILE_PRE_OCR_UNCLEANED:
        write_pandas(df, SAVE_PATH_PRE_OCR_UNCLEANED)
    print_telegram(f'Amount of data before cleaning: {len(df.index)}')
    df["target"] = df["target"].str.split(".")
    df = df.explode('target').reset_index(drop=True)

    df["target"] = df["target"].str.split(";")
    df = df.explode('target').reset_index(drop=True)
    print_telegram(f'Amount of data after exploding: {len(df.index)}')
    # print(df)
    df = clean_dataframe(df)
    print_telegram(f'Amount of data after cleaning: {len(df.index)}')
    if WRITE_FILE_PRE_OCR_CLEANED:
        write_pandas(df, SAVE_PATH_PRE_OCR_CLEANED)
    return df
