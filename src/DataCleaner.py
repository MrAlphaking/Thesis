import logging
import os
import xml.etree.ElementTree as ET
import regex as re
import pandas as pd
from src.utils.Delpher import Delpher

MIN_CHARACTERS = 5
MAX_CHARACTERS = 10000
READ_FROM_FILE = True


BASE_PATH = '../../data/Ground Truth/'
SAVE_FILE_PATH = BASE_PATH + "total"

delpher = Delpher()
##### Utils

def remove_duplicates(data):
    seen = set()
    result = []
    for line in data:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return result

def clean_line(line, df):
    # Check for min and max length
    # print(line)
    if len(line) < MIN_CHARACTERS:
        return
    # Check for any digit in the string
    elif any(char.isdigit() for char in line):
        return
    line = line.replace("\n", "")
    line = line.replace("<FI>", "")
    # Remove trailing spaces
    line = line.strip()
    line = re.sub('[^A-Za-z0-9,.\s]+', '', line)
    # return_list.append(line)
    # df.loc[i] = ['name' + str(i)] + list(randint(10, size=2))
    return

def clean_dataframe(df):
    df['target'] = df['target'].apply(lambda x: str(x))
    df['target'] = df['target'].apply(lambda x: x.strip())
    df['target'] = df['target'].apply(lambda x: re.sub('[^A-Za-z0-9,.\s]+', '', x))

    df = df[df['target'].apply(lambda x: x.count(' ') > MIN_CHARACTERS)]
    df = df[df['target'].apply(lambda x: x.count(' ') < MAX_CHARACTERS)]
    df = df[df['target'].apply(lambda x: not(any(char.isdigit() for char in x)))]
    df = df[df['year'].apply(lambda x: x != '0000')]
    df.reset_index(drop=True)
    print(df)
    return df
    # return df.loc[df.target.str.contains('[^A-Za-z0-9,.\s:!]+'), :]

def clean_data(data):
    return_list = []
    for line in data:
        clean_line(line, return_list)
    return_list = remove_duplicates(return_list)
    return return_list

def merge(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list
def get_txt(path):
    with open(f'{BASE_PATH}{path}', encoding="utf8", errors="ignore") as f:
        lines = f.read().replace("\n", " ").split(".")
        return lines

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
    logging.info(f'Writing to file: {path}')
    df.to_csv(path)

def read_pandas(path):
    logging.info(f'Reading from file: {path}')

    return pd.read_csv(path)

def create_year_list(year, count):
    return [year for i in range(count)]

##### Code

def get_statenvertaling():
    lines = get_txt('Statenvertaling - 1637')
    years = create_year_list(1637, len(lines))
    df = pd.DataFrame(merge(lines, years), columns=["target", "year"])
    return df
    # print(df.to_string())

def get_impact(path):
    logging.info(f'Reading in {path}')
    df = pd.read_excel(f'{BASE_PATH}xlsx/impact_{path.replace(" ", "_").lower()}.xlsx')
    path = f'../../data/Ground Truth/{path}/xml/'
    lines = []

    for file in os.listdir(path):
        Did = int(file.replace(".xml", "").lstrip('0'))
        year = df.loc[df['Did'] == Did].reset_index(drop=True).at[0, 'Dyear']
        filename = path + file
        results = get_xml_element(filename, element="Unicode")
        # Flatten list
        results = [item for sublist in results for item in sublist]
        results = merge(results, create_year_list(year, len(results)))
        lines = [*lines, *results]

    return_frame = pd.DataFrame(lines, columns=["target", "year"])
    return return_frame

def get_dbnl_books():
    logging.info(f'Reading in Books 2')
    path = f'../../data/Ground Truth/Books 2/TXT'

    df = pd.read_excel(f'{BASE_PATH}xlsx/Metadata_DBNL_OCR_v1.xlsx')
    lines = []
    for file in os.listdir(path):
        Did = file.replace(".txt", "")
        year = df.loc[df['ti_id'] == Did].reset_index(drop=True).at[0, 'jaar']
        results = get_txt(f'Books 2/TXT/{file}')
        results = [item for sublist in results for item in sublist]
        results = merge(results, create_year_list(year, len(results)))
        lines = [*lines, *results]

    return_frame = pd.DataFrame(lines, columns=["target", "year"])
    return return_frame

def get_historical_newspaper():
    logging.info(f'Reading in historical newspapers')
    df = pd.read_csv(f'{BASE_PATH}Newspapers 2/historical_newspaper_groundtruth.csv')
    years = []
    for item in list(df["identifier"]):
        item = re.sub('_[0-9][0-9][0-9].jp2_ocr', '', item).replace("_", ":").lower() + ":mpeg21"
        year = delpher.get_year(item)
        years.append(year)

    df['year'] = years
    df = df.drop(['Unnamed: 0', 'identifier', 'ocr_text'], axis=1)
    df = df.rename(columns={'gt text': 'target'})
    return df

def get_17thcenturynewspaper():
    logging.info(f'Reading in 17th century newspapers')
    df = pd.read_csv(f'{BASE_PATH}17thcenturynewspapers.csv', compression='gzip')
    years = []
    for item in list(df["identifier"]):
        item = re.sub(':a[0-9][0-9][0-9][0-9]', '', item)
        year = Delpher.get_year(item)
        years.append(year)

    df['year'] = years
    df = df.drop(['Unnamed: 0', 'identifier', 'ocr_text'], axis=1)
    df = df.rename(columns={'gt text': 'target'})

    return df

def get_data():
    if READ_FROM_FILE:
        df = read_pandas(SAVE_FILE_PATH)
        print(df.head())
    else:
        impact_newspapers = get_impact('Newspapers')
        impact_books = get_impact('Books')
        impact_parliamentary_proceedings = get_impact('Parliamentary Proceedings')
        impact_radiobulletins = get_impact('Radio Bulletins')
        statenvertaling = get_statenvertaling()
        # dbnl_books = get_dbnl_books()
        # historical_newspaper = get_historical_newspaper()
        # seventeenth_century_newspaper = get_17thcenturynewspaper()

        df = [impact_newspapers, impact_books, impact_parliamentary_proceedings, impact_radiobulletins, statenvertaling]#, historical_newspaper, seventeenth_century_newspaper]
        df = pd.concat(df)

        write_pandas(df, SAVE_FILE_PATH)

    logging.info(f'Amount of data before cleaning: {len(df.index)}')
    df["target"] = df["target"].str.split(".")
    df = df.explode('target').reset_index(drop=True)
    logging.info(f'Amount of data after exploding: {len(df.index)}')
    df = clean_dataframe(df)
    logging.info(f'Amount of data after cleaning: {len(df.index)}')

    print(df.head())
    return df