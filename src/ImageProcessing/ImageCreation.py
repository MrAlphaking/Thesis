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

    def get_text_dimensions(self, text_string, font):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)

    def get_concat_h(self, im1, im2):
        """
        Concatenates 2 images horizontally, and returns the concatenated result
        :param im1: The first image
        :param im2: The second image 
        :return: The concatenated result
        """
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    def get_concat_v(self, im1, im2):
        """
        Concatenates 2 images horizontally, and returns the concatenated result
        :param im1: The first image
        :param im2: The second image 
        :return: The concatenated result
        """
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

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
        org_img = Image.open(f'{path}/{chosen_file}')
        img = org_img

        FONT_FAMILY = "../fonts/BreitkopfFraktur.ttf"
        FONT_SIZE = 25
        font = ImageFont.truetype(FONT_FAMILY, FONT_SIZE)
        text_width, text_height = self.get_text_dimensions(ocr_text, font)

        while img.size[0] < text_width + 80:
            img = self.get_concat_h(img, org_img)

        I1 = ImageDraw.Draw(img)
        I1.text((40,30), ocr_text, font=font, fill=(0,0,0))

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

        for index, row in tqdm(df.iterrows(), token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Creating images: "):
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
