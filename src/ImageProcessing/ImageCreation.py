# Importing the PIL library
import logging
logging.getLogger('PIL').setLevel(logging.WARNING)
from PIL import Image
from PIL import ImageDraw
from src.utils.Settings import IMAGE_PATH_BLANK, IMAGE_WRITE_BLANK
from PIL import ImageFont
import textwrap

class ImageCreation:
    def __init__(self):
        self.image_path = IMAGE_PATH_BLANK
        self.output_path = IMAGE_WRITE_BLANK
    def getBackground(self, time_period=None):
        if time_period is None:
            return Image.open(self.image_path)

    def getImage(self, ocr_text, index=None):
        img = self.getBackground()
        textwrapped = textwrap.wrap(ocr_text, width=75)
        I1 = ImageDraw.Draw(img)
        # myFont = ImageFont.truetype('../fonts/BreitkopfFraktur.ttf', 10)
        y = 10
        for line in textwrapped:
            I1.text((10,y), line, fill=(0, 0, 0))
            y += 15
        # I1.text((10, 10), ocr_text, font=myFont, fill=(0, 0, 0))
        if index is None:
            img.save(self.output_path + '.jpg')
            return self.output_path + '.jpg'
        else:
            img.save(self.output_path + str(index) + '.jpg')
            return self.output_path + str(index) + '.jpg'
