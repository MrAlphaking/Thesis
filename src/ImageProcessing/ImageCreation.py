# Importing the PIL library
import logging
logging.getLogger('PIL').setLevel(logging.WARNING)
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap

class ImageCreation:
    def __init__(self, image_path, output_path):
        self.image_path = image_path
        self.output_path = output_path
    def getBackground(self, time_period=None):
        if time_period is None:
            return Image.open(self.image_path)

    def getImage(self, ocr_text):
        img = self.getBackground()
        textwrapped = textwrap.wrap(ocr_text, width=75)
        # print(textwrapped)
        I1 = ImageDraw.Draw(img)
        # myFont = ImageFont.truetype('../fonts/BreitkopfFraktur.ttf', 10)
        y = 10
        for line in textwrapped:
            I1.text((10,y), line, fill=(0, 0, 0))
            y += 15
        # I1.text((10, 10), ocr_text, font=myFont, fill=(0, 0, 0))
        img.save(self.output_path)
        return self.output_path