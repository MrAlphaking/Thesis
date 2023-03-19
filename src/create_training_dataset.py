import os

from OCR import *
from src.ImageProcessing.ImageProcessor import ImageProcessor
from src.utils.Delpher import Delpher

import DataCreator

if __name__ == "__main__":
    delpher = Delpher()
    delpher.download_images_period(1630, 1990, maximum_records=100, step_size=1)
    imageProcessor = ImageProcessor(SAVE_PATH_DOWNLOAD_IMAGE)
    imageProcessor.create_rectangles(80, 0, 200)

    df = DataCreator.get_dataframe()





