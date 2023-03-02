# Importing the PIL library
import logging
import os

logging.getLogger('PIL').setLevel(logging.WARNING)
from PIL import Image
from PIL import ImageDraw
from tqdm.contrib.telegram import tqdm
from src.utils.Settings import IMAGE_PATH_BLANK, IMAGE_WRITE_BLANK
from src.utils.Util import *
from PIL import ImageFont
import textwrap
import threading
import time
import psutil
class ImageCreation:
    def __init__(self):
        self.image_path = IMAGE_PATH_BLANK
        self.output_path = IMAGE_WRITE_BLANK
    def getBackground(self, time_period=None):
        if time_period is None:
            return Image.open(self.image_path)

    def create_image(self, index, ocr_text, image_list):
        img = self.getBackground()
        textwrapped = textwrap.wrap(ocr_text, width=75)
        I1 = ImageDraw.Draw(img)
        # myFont = ImageFont.truetype('../fonts/BreitkopfFraktur.ttf', 10)
        y = 10
        for line in textwrapped:
            I1.text((10,y), line, fill=(0, 0, 0))
            y += 15
        # I1.text((10, 10), ocr_text, font=myFont, fill=(0, 0, 0))
        # if index is None:
        #     path = self.output_path + '.jpg'
        # else:
        path = self.output_path + str(index) + '.jpg'
        img.save(path)
        image_list.append((index, path))

    def remove_image_list(self, image_list):
        for image in tqdm(image_list, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc='Removing Images:'):
            os.remove(image)

    def create_image_list(self, ocr_text_list):
        images = []
        threads = list()
        for index, text in enumerate(tqdm(ocr_text_list, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Creating images:")):
            # images.append((index, self.create_image(text, index=index)))
            while psutil.cpu_percent() >= 100:
                # print("Sleep")
                time.sleep(0.01)

            x = threading.Thread(target=self.create_image, args=(index, text, images,))
            threads.append(x)
            x.start()

        for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Joining threads"):
            thread.join()
        images.sort(key=lambda x: x[0])
        return list(zip(*images))[1]
