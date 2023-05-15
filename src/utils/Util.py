import logging
import requests
from src.utils.Settings import *
import pandas as pd
import inspect
from tqdm.contrib.telegram import tqdm
import xml.etree.ElementTree as ET


def get_xml_element(filename, element="Unicode"):
    lines = []
    root = ET.parse(filename).getroot()
    for element in root.attrib:
        if "Location" in element:
            location = root.attrib[element].split(" ")[0]
            break

    location = "{" + location + "}"
    for children in root.findall(f".//{location}Unicode"):
        text = children.text.replace("\n", " ")
        text = text.split(".")
        lines.append(text)
    # print(lines)
    return lines
def write_pandas(df, path):
    print_telegram(f'Writing to file: {path}')
    df.to_csv(path, index=False)

def read_pandas(path):
    print(f'Reading from file: {path}')
    return pd.read_csv(path)

def progress_bar(item_list, desc=""):
    return tqdm(item_list, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc=desc, miniters=int(len(item_list)/100), mininterval=1, maxinterval=float("inf"))
def print_telegram(text):
    # stack = inspect.stack()
    # if "self" in stack[1][0].f_locals:
    #     the_class = stack[1][0].f_locals["self"].__class__.__name__
    #     the_method = stack[1][0].f_code.co_name
    #     text = f'{the_class}, {the_method}: {text}'

    print(text)

    if TELEGRAM_BOOLEAN:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={text}"
        requests.get(url).json()
