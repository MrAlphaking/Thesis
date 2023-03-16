# Importing the PIL library
import logging
import os
import random

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
import cv2
import numpy as np


class ImageCreation:
    def __init__(self):
        self.image_path = IMAGE_PATH_BLANK
        self.output_path = IMAGE_WRITE_BLANK

    def create_image(self, index, ocr_text, year, image_list):
        """
        This function takes as input an OCR text and turns it into an image.
        :param index: This is used so the entire list can be kept in the right order when using threads.
        :param ocr_text: The text to be turned into an image.
        :param image_list: The list to add the image to. This is a pass by reference list, used by multiple threads at once.
        """
        if year == "0000":
            year = random.randint(1637,1900)
        path = f'{SAVE_PATH_BACKGROUND_IMAGE}/{year}'
        files = os.listdir(path)
        # print(f'{files}, [{len(files)}]')
        chosen_file = files[random.randint(0, len(files)-1)]
        org_img = cv2.imread(f'{path}/{chosen_file}')
        img = org_img

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1.0
        thickness = 2
        size, _ = cv2.getTextSize(ocr_text, font, fontScale, thickness)
        text_width, text_height = size


        while img.shape[1] < text_width + 80:
            img = np.concatenate((img, org_img), axis=1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        # ft = cv2.freetype.createFreeType2()
        # ft.loadFontData(fontFileName='../../fonts/BreitkopfFraktur.tff',
        #                 id=0)
        # ft.putText(img=img,
        #            text=ocr_text,
        #            org=(20,20),
        #            fontScale=fontScale,
        #            color=(255, 255, 255),
        #            thickness=thickness,
        #            line_type=cv2.LINE_AA)


        # img = cv2.putText(img, ocr_text, (40,30), font,
        #                     fontScale, (0,0,0), thickness, cv2.LINE_AA)

        I1 = ImageDraw.Draw(img)
        I1.text((40,30), ocr_text, fontScale=fontScale, thickness= thickness, fill=(255,255,255))

        path = self.output_path + str(index) + '.jpg'
        img.save(path)
        image_list.append((index, path))

    def remove_image_list(self, image_list):
        """
        Takes as input a list of images and subsequently removes those images.
        :param image_list: The images to be removed.
        """

        for image in tqdm(image_list, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc='Removing Images:'):
            os.remove(image)

    def create_image_list(self, df):
        """
        Takes as input a list of text, and turns it into images which can later be used to be OCR'ed.
        :param df: The dataframe containing all the text
        :return: The list of images
        """
        images = []
        threads = list()

        for index, row in tqdm(df.iterrows(), token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Creating images:"):
            # images.append((index, self.create_image(text, index=index)))
            while psutil.cpu_percent() >= 100:
                # print("Sleep")
                time.sleep(0.01)

            x = threading.Thread(target=self.create_image, args=(index, row['target'], row['year'], images,))
            threads.append(x)
            x.start()

        for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Joining threads"):
            thread.join()
        images.sort(key=lambda x: x[0])
        return list(zip(*images))[1]
