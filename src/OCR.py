from PIL import Image
import platform
import pytesseract

class OCR:
    def __init__(self):
        print("OCR class has been made")


        if platform.system() == "Linux":
            print("here")
            pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        else:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def get_ocr(self, image_path):
        return pytesseract.image_to_string(Image.open(image_path))