import logging
import requests
from src.utils.Settings import *
import pandas as pd
import inspect

def write_pandas(df, path):
    logging.info(f'Writing to file: {path}')
    df.to_csv(path)

def read_pandas(path):
    logging.info(f'Reading from file: {path}')
    return pd.read_csv(path)

def print_telegram(text):
    stack = inspect.stack()
    if "self" in stack[1][0].f_locals:
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name
        text = f'{the_class}, {the_method}: {text}'

    print(text)

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={text}"
    requests.get(url).json()
