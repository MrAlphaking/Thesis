import os

from OCR import *
from src.ImageProcessing.ImageProcessor import ImageProcessor
from src.utils.Delpher import Delpher

import DataCreator

if __name__ == "__main__":
    # delpher = Delpher()
    # delpher.download_images_period(1700, 1710, maximum_records=1000, step_size=10)
    # imageProcessor = ImageProcessor(SAVE_PATH_DOWNLOAD_IMAGE)
    # imageProcessor.test()
    # imageProcessor.create_rectangles(80, 0, 200)
    # imageProcessor.clean_rectangles(SAVE_PATH_BACKGROUND_IMAGE)
    # imageProcessor.create_image_collage(SAVE_PATH_BACKGROUND_IMAGE)
    df = DataCreator.get_dataframe()






