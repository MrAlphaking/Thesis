from DataCleaner import *
from TextStatistics import *
from OCR import *
from src.ImageProcessing.ImageCreation import *
import logging
import sys
# image_path = "../images/background.jpeg"
# output_path = "../images/background-edited.jpeg"

root = logging.getLogger()
root.setLevel(logging.DEBUG)
# root.disabled = True

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

image_path = "../images/white.jpg"
output_path = "../images/white-edited.jpg"
ImageCreation = ImageCreation(image_path, output_path)

def get_dataframe():
    ocr = OCR()
    df = get_data().head(10).drop('Unnamed: 0', axis=1)
    statistics = TextStatistics()
    sources = []

    for index, row in df.iterrows():
        target = row['target']
        ImageCreation.getImage(target)
        source = ocr.get_ocr(output_path).strip("\n")
        sources.append(source)
        logging.info(f"{target} -> {source}")

    df['source'] = sources
    print(df)
    print(df.head())
    print(df.columns)

get_dataframe()