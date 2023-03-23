# Importing the PIL library
import logging
import os
import random

logging.getLogger('PIL').setLevel(logging.WARNING)
from PIL import Image
from PIL import ImageDraw, ImageEnhance, ImageFilter
from tqdm.contrib.telegram import tqdm
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
        print_telegram("ImageCreation class")
        # self.image_path = IMAGE_PATH_BLANK
        # self.output_path = IMAGE_WRITE_BLANK

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

    # def create_image(self, index, ocr_text, year, image_list):

    def get_time_period_path(self, year):
        """
        Since the folder structure is begin_year-end_year for the background images, it should be identified which time period to choose.
        :param year: The year for which to take the correct path.
        :return: The correct path
        """
        for path in os.listdir(SAVE_PATH_BACKGROUND_IMAGE):
            years = path.split("-")
            if int(years[0]) <= year and int(years[1]) > year:
                return f'{SAVE_PATH_BACKGROUND_IMAGE}/{path}'
        random_path = random.choice(os.listdir(SAVE_PATH_BACKGROUND_IMAGE))
        print_telegram(f"No correct path could be found for year: {year}, thus returning {random_path} instead")
        return f'{SAVE_PATH_BACKGROUND_IMAGE}/{random_path}'

    def get_correct_font(self, year):
        """
        The goal of this function is to return the correct font type, for the corresponding year.
        :param year:
        :return:
        """

        if year < 1650:
            FONT_FAMILY = "../fonts/textur.ttf"
            FONT_SIZE = 14
        elif year >= 1650 and year < 1700:
            fonts = ["../fonts/textur.ttf"]#, "../fonts/jenson-roman.ttf"]
            FONT_FAMILY = random.choice(fonts)
            FONT_SIZE = 14
        elif year >= 1700: #and year < 1931:
            FONT_FAMILY = "../fonts/caslon.ttf"
            FONT_SIZE = 12
        # elif year >= 1931:
        #     FONT_FAMILY = "../fonts/times-new-roman.ttf"
        #     FONT_SIZE = 13

        print_telegram(FONT_FAMILY)
        font = ImageFont.truetype(FONT_FAMILY, FONT_SIZE)
        return font

    def apply_blur(self, img, year):
        if year < 1700:
            img = img.filter(ImageFilter.BoxBlur(0.04))
        elif year >= 1700 and year < 1931:
            img = img.filter(ImageFilter.BoxBlur(0.15))
        # elif year >= 1931:
        #     img = img.filter(ImageFilter.BoxBlur(0.20))

        return img


    def create_image(self, index, ocr_text, year):
        """
        This function takes as input an OCR text and turns it into an image.
        :param index: This is used so the entire list can be kept in the right order when using threads.
        :param ocr_text: The text to be turned into an image.
        :param image_list: The list to add the image to. This is a pass by reference list, used by multiple threads at once.
        """
        # if year == "0000":
        #     year = random.randint(1637,1900)
        path = self.get_time_period_path(year)
        files = os.listdir(path)
        # print(f'{files}, [{len(files)}]')
        chosen_file = files[random.randint(0, len(files)-1)]
        org_img = Image.open(f'{path}/{chosen_file}')
        img = org_img

        font = self.get_correct_font(year)
        text_width, text_height = self.get_text_dimensions(ocr_text, font)

        while img.size[0] < text_width + 80:
            img = self.get_concat_h(img, org_img)

        I1 = ImageDraw.Draw(img)
        I1.text((40,30), ocr_text, font=font, fill=(0,0,0))
        path = f'../images/{index}.jpg'
        img.save(path)

        for i in range(round(img.size[0] * img.size[1] / 140 )):
            img.putpixel(
                (random.randint(0, img.size[0] - 1), random.randint(0, img.size[1] - 1)),
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            )
        img = self.apply_blur(img, year)
        path = f'../images/noise-{index}.jpg'
        img.save(path)
        return img

        # image_list.append((index, path))

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

        for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Joining threads of creating images: "):
            thread.join()
        images.sort(key=lambda x: x[0])
        return list(zip(*images))[1]


