from DataCleaner import *
from TextStatistics import *
from OCR import *
from ImageCreation import *
import pandas as pd
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

ocr = OCR()
data = get_data()
statistics = TextStatistics()
statistics.print_wordcount(data)

# print(data)
corrections = []

for target in data[:100]:
    # print(target)
    ImageCreation.getImage(target)
    source = ocr.get_ocr(output_path).strip("\n")
    corrections.append((source, target))
    logging.info(f"{source} -> {target}")

df = pd.DataFrame(corrections, columns = ["source", "target"])
print(df)
