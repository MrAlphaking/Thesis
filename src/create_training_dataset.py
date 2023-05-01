import os

from OCR import *
from src.ImageProcessing.ImageProcessor import ImageProcessor
from src.utils.Delpher import Delpher

import DataCreator

if __name__ == "__main__":
    # delpher = Delpher()
    # delpher.download_images_period(1630, 1990, maximum_records=20, step_size=10)
    # imageProcessor = ImageProcessor(SAVE_PATH_DOWNLOAD_IMAGE)
    # imageProcessor.test()
    # imageProcessor.create_rectangles(80, 0, 200)
    # imageProcessor.clean_rectangles(SAVE_PATH_BACKGROUND_IMAGE)

    df = DataCreator.get_dataframe()






