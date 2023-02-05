# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class ImageCreation:
    def __init__(self, image_path, output_path):
        self.image_path = image_path
        self.output_path = output_path


    def getBackground(self, time_period=None):
        if time_period is None:
            return Image.open(self.image_path)

    def getImage(self, ocr_text):
        img = self.getBackground()
        I1 = ImageDraw.Draw(img)
        # myFont = ImageFont.truetype('../fonts/BreitkopfFraktur.ttf', 10)
        I1.text((10, 10), ocr_text, fill=(0, 0, 0))
        # I1.text((10, 10), ocr_text, font=myFont, fill=(0, 0, 0))
        img.save(self.output_path)