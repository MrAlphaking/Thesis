from PIL import Image

import pytesseract

class OCR:
    def __init__(self):
        print("OCR class has been made")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def get_ocr(self, image_path):
        return pytesseract.image_to_string(Image.open(image_path))