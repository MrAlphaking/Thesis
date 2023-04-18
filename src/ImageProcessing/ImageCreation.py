# Importing the PIL library
import logging
import os
import random

from OCR import OCR

logging.getLogger('PIL').setLevel(logging.WARNING)
from PIL import Image
from PIL import ImageDraw, ImageFilter
from src.utils.Util import *
from PIL import ImageFont
import threading
import time
import psutil
import textwrap


class ImageCreation:
    def __init__(self):
        print_telegram("ImageCreation class")
        # self.image_path = IMAGE_PATH_BLANK
        # self.output_path = IMAGE_WRITE_BLANK

    def get_text_dimensions(self, text_string, font):
        # https://stackoverflow.com/a/46220683/9263761
        try:
            ascent, descent = font.getmetrics()

            text_width = font.getmask(text_string).getbbox()[2]
            text_height = font.getmask(text_string).getbbox()[3] + descent
            return (text_width, text_height)

        except:
            print(font)
            print(f'String: {text_string}')
            regex_string = '[^A-Za-z0-9,.;\s]+'
            # print(len(text_string.strip()))
            # print(len(text_string))

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
            if int(years[0]) <= int(year) and int(years[1]) > int(year):
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

        global FONT_FAMILY
        if year < 1650:
            FONT_FAMILY = "../fonts/caslon.ttf"
            FONT_SIZE = 15
        elif year >= 1650 and year < 1700:
            fonts = ["../fonts/caslon.ttf"]  # , "../fonts/jenson-roman.ttf"]
            FONT_FAMILY = random.choice(fonts)
            FONT_SIZE = 15
        elif year >= 1700:  # and year < 1931:
            FONT_FAMILY = "../fonts/caslon.ttf"
            FONT_SIZE = 15
        # elif year >= 1931:
        #     FONT_FAMILY = "../fonts/times-new-roman.ttf"
        #     FONT_SIZE = 13

        # print_telegram(FONT_FAMILY)
        font = ImageFont.truetype(FONT_FAMILY, FONT_SIZE)
        if FONT_FAMILY == "../fonts/caslon.ttf":
            return 3, font
        elif FONT_FAMILY == "../fonts/textur.ttf":
            return -1, font

    def apply_blur(self, img, year):
        if year < 1700:
            img = img.filter(ImageFilter.BoxBlur(0.01))
        elif year >= 1700 and year < 1931:
            img = img.filter(ImageFilter.BoxBlur(0.04))
        # elif year >= 1931:
        #     img = img.filter(ImageFilter.BoxBlur(0.20))

        return img

    # def get_wrapped_text(self, text: str, font: ImageFont.ImageFont,
    #                      line_length: int):
    #     lines = ['']
    #     for word in text.split():
    #         line = f'{lines[-1]} {word}'
    #         # print(line)
    #         if font.getlength(line) <= line_length:
    #             lines[-1] = line
    #         else:
    #             lines.append(word)
    #     return '\n'.join(lines)

    def get_wrapped_text(self, text, font, line_length, text_spacing):
        lines = ['']

        y_spacing = font.getsize("A")[1] + text_spacing
        y_spacing_list = []
        current_spacing = y_spacing
        # y_spacing_list.append(current_spacing)
        print(y_spacing)
        previous_length = 0
        print(f'length: 0')
        for sentence in text:
            print(sentence)
            for word in sentence.split(" "):
                line = f'{lines[-1]} {word}'
                # print(line)

                if font.getlength(line) <= line_length:
                    lines[-1] = line
                else:
                    lines.append(word)
                    # current_spacing += y_spacing

            lines[-1] = f'{lines[-1]}'
            print(f'{previous_length} -> {len(lines)}')

            current_spacing += y_spacing * (len(lines) - previous_length)
            previous_length = len(lines)
            y_spacing_list.append(current_spacing)
            lines.append('')

        print(lines)

            # y_spacing_list.append(lines[-1].count("\n") * y_spacing + y_spacing_list[-1])
        return y_spacing, y_spacing_list, '\n'.join(lines)

    # def add_lines(self, ocr_text):
    #     return_text = ""
    #     for i in range(10):
    #         return_text += f'{ocr_text}'
    #     return return_text
    # def merge_lines(self, ocr_text):
    #     return_text = ""
    #     for text in ocr_text:
    #         return_text += f'{text}'
    #     return return_text
    
    def create_background(self, year, width, height):
        year = int(year)
        if year == "0000":
            year = random.randint(1637,1900)
        path = self.get_time_period_path(year)
        files = os.listdir(path)
        chosen_file = files[random.randint(0, len(files) - 1)]
        org_img = Image.open(f'{path}/{chosen_file}')
        img = org_img

        while img.size[0] < width:
            img = self.get_concat_h(img, org_img)
        org_img = img
        while img.size[1] < height:
            img = self.get_concat_v(img, org_img)

        return img

    def apply_noise(self, img):
        for i in range(round(img.size[0] * img.size[1] / 140)):
            img.putpixel(
                (random.randint(0, img.size[0] - 1), random.randint(0, img.size[1] - 1)),
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            )
        return img

    def create_image_from_df(self, index, background, width, height, ocr_text, year):
        """
        This function takes as input an OCR text and turns it into an image. :param index: This is used so the entire
        list can be kept in the right order when using threads. :param ocr_text: The text to be turned into an image.
        :param image_list: The list to add the image to. This is a pass by reference list, used by multiple threads
        at once.
        """

        img = background
        # img_size = img.size
        # ocr_text = self.merge_lines(ocr_text)
        text_spacing = 4
        font_offset, font = self.get_correct_font(year)
        y_spacing, y_spacing_list, ocr_text = self.get_wrapped_text(ocr_text, font, width, text_spacing)

        #text_width, text_height = self.get_text_dimensions(ocr_text, font)
        # offset = (40, 30)
        I1 = ImageDraw.Draw(img)
        I1.text((40, 30), ocr_text, font=font, fill=(0, 0, 0), spacing=text_spacing, align='center')
        print(y_spacing_list)
        print(len(y_spacing_list))
        for spacing in y_spacing_list:
            y = spacing + 0.5 * text_spacing + 0.5 * y_spacing + font_offset
            I1.line([(0,y), (img.size[0], y)])
        path = f'../images/{index}-{year}.png'
        img.save(path)

        # img = self.apply_blur(img, year)
        # img = self.apply_noise(img)
        img.save(path)
        ocr = OCR()
        print(ocr.get_text(img))
        img.show()
        return img
    def create_image2(self, index, ocr_text, year):
        """
        This function takes as input an OCR text and turns it into an image. :param index: This is used so the entire
        list can be kept in the right order when using threads. :param ocr_text: The text to be turned into an image.
        :param image_list: The list to add the image to. This is a pass by reference list, used by multiple threads
        at once.
        """

        x_width = 1772
        y_width = 3000





        ocr_text = self.add_lines(ocr_text)
        # print(ocr_text)
        # print(word_list)
        year = int(year)
        # if year == "0000":
        #     year = random.randint(1637,1900)
        path = self.get_time_period_path(year)
        files = os.listdir(path)
        # print(f'{files}, [{len(files)}]')
        chosen_file = files[random.randint(0, len(files) - 1)]
        org_img = Image.open(f'{path}/{chosen_file}')
        img = org_img

        font = self.get_correct_font(year)
        ocr_text = self.get_wrapped_text(ocr_text, font, x_width)
        text_width, text_height = self.get_text_dimensions(ocr_text, font)

        while img.size[0] < x_width:
            img = self.get_concat_h(img, org_img)

        org_img = img

        while img.size[1] < y_width:
            img = self.get_concat_v(img, org_img)


        I1 = ImageDraw.Draw(img)
        I1.text((40, 30), ocr_text, font=font, fill=(0, 0, 0), align='center')
        path = f'../images/{index}.jpg'
        img.save(path)

        for i in range(round(img.size[0] * img.size[1] / 140)):
            img.putpixel(
                (random.randint(0, img.size[0] - 1), random.randint(0, img.size[1] - 1)),
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            )
        img = self.apply_blur(img, year)
        path = f'../images/noise-{index}.png'
        img.save(path)
        return img

        image_list.append((index, path))

    def remove_image_list(self, image_list):
        """
        Takes as input a list of images and subsequently removes those images.
        :param image_list: The images to be removed.
        """

        for image in tqdm(image_list, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc='Removing Images:'):
            os.remove(image)

    # def create_image_list(self, df):
    #     for index, row in progress_bar(df.iterrows, desc="Creating images: "):


    def create_image_list2(self, df):
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

            x = threading.Thread(target=self.create_image2, args=(index, row['target'], row['year'], images,))
            threads.append(x)
            x.start()

        for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID,
                           desc="Joining threads of creating images: "):
            thread.join()
        images.sort(key=lambda x: x[0])
        return list(zip(*images))[1]

