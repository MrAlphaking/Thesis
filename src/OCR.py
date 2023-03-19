from PIL import Image
import platform
import pytesseract
import threading
import tesserocr
from src.utils.Util import *
from tqdm.contrib.telegram import tqdm
import psutil
import time
class OCR:
    def __init__(self):
        """
        Initializes an instance of the OCR class, which allows to get the OCR data of a certain image.

        :param None:
        """
        print_telegram("OCR class has been made")
        if platform.system() == "Linux":
            print("here")
            pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        else:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # def get_ocr(self, image_path):
    #     """
    #     This function uses the pytesseract library in order to return the ocr output of a given image path.
    #
    #     :param image_path: The image to obtain the ocr of.
    #     :return: The obtained ocr of the image.
    #     """
    #     try:
    #         pytesseract
    #         return pytesseract.image_to_string(Image.open(image_path))
    #     except:
    #         time.sleep(1)
    #         return self.get_ocr(image_path)

    def add_ocr(self, index, image_path, ocr):
        """
        This function is used by the get_ocr_list function to add the ocr data of a certain image_path, by using the tesserocr api.

        :param index: The index of the data point in the dataset, used for order preservation
        :param image_path: The path leading to the image to be ocr'ed
        :param ocr: A list that
        :param api: The api that is utilized in order to obtain the ocr data.
        """
        image = Image.open(image_path)
        ocr_text = tesserocr.image_to_text(image).replace('\n', "")
        ocr.append((index, ocr_text))

    # def get_ocr_list(self, path_list):
    #     """
    #     Creates a list of ocr data, given a list of images
    #
    #     :param path_list: A list of images, to be ocr'ed
    #     :return: A list containing the ocr data of all the images.
    #     """
    #     ocr = []
    #     threads = list()
    #     with tesserocr.PyTessBaseAPI(path='../tessdata/', lang='nld') as api:
    #         for index, path in enumerate(tqdm(path_list, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Getting OCR inputs: ")):
    #             while threading.active_count() > MAX_THREADING_COUNT:
    #                 time.sleep(0.1)
    #
    #             x = threading.Thread(target=self.add_ocr, args=(index, path, ocr, api,))
    #             threads.append(x)
    #             x.start()
    #
    #     for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Joining threads"):
    #         thread.join()
    #
    #     print(ocr)
    #     ocr.sort(key=lambda x: x[0])
    #     return list(zip(*ocr))[1]

    def get_ocr_list(self, path_list):
        """
        Creates a list of OCR data, given a list of images.

        :param path_list: A list of image paths to be OCR-ed.
        :type path_list: list of str
        :return: A list containing the OCR data of all the images.
        :rtype: list of str
        """
        ocr = []
        threads = list()

        for index, img in enumerate(tqdm(path_list, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID)):
            while psutil.cpu_percent() >= 100:
                time.sleep(0.01)
            x = threading.Thread(target=self.add_ocr, args=(index, img, ocr,))
            threads.append(x)
            x.start()

        for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, desc="Joining threads"):
            thread.join()
        print(ocr)
        ocr.sort(key=lambda x: x[0])
        return list(zip(*ocr))[1]

if __name__ == "__main__":
    ocr = OCR()
    ocr.get_ocr_list2(['../images/run/white-edited-2.jpg'])