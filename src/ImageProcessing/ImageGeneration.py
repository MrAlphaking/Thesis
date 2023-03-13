import os
import time

from tesserocr import PyTessBaseAPI, RIL
from PIL import Image
import pytesseract
import cv2
from src.utils.Util import *
import tqdm
from pytesseract import Output
import matplotlib.pyplot as plt
import keras_ocr
import numpy as np
def remove_text(image_path):
    # read the image and get the dimensions
    # img = cv2.imread(image_path)
    # h, w, _ = img.shape  # assumes color image
    #
    # # run tesseract, returning the bounding boxes
    # boxes = pytesseract.image_to_boxes(img)  # also include any config options you use
    #
    # # draw the bounding boxes on the image
    # for b in boxes.splitlines():
    #     b = b.split(' ')
    #     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    #
    # # show annotated image and wait for keypress
    # cv2.imshow(image_path, img)
    #
    # cv2.waitKey(0)

    image = Image.open(image_path)
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    with PyTessBaseAPI(path='../../tessdata/', lang='nld') as api:
        api.SetImage(image)
        # print(api.GetUTF8Text())
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        print('Found {} textline image components.'.format(len(boxes)))
        print(boxes)
        for index, (im, box, _, _) in enumerate(progress_bar(boxes, desc='Boxes: ')):

            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            img = cv2.rectangle(img, (int(box['x']), h - int(box['y'])), (int(box['w']), h - int(box['h'])), (0, 255, 0), 2)

            # api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            # ocrResult = api.GetUTF8Text()
            # conf = api.MeanTextConf()
            # print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
            #       "confidence: {1}, text: {2}".format(i, conf, ocrResult, **box))

    cv2.imshow(image_path, img)
    print('Done')
    cv2.waitKey(0)
        # api.SetImageFile(image)
        # print(api.GetUTF8Text())
        # ocr_text = tesserocr.image_to_text(image).replace('\n', "")
        # api.getUTF8(image)


        # ocr.append((index, ocr_text))


def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2) / 2)
    y_mid = int((y1 + y2) / 2)
    return (x_mid, y_mid)


import math
import psutil


def remove_text2(image_path):

    pipeline = keras_ocr.pipeline.Pipeline()
    # read image from the an image path (a jpg/png file or an image url)
    img = keras_ocr.tools.read(image_path)
    # Prediction_groups is a list of (word, box) tuples
    prediction_groups = pipeline.recognize([img])
    # print(prediction_groups)
    # print image with annotation and boxes
    # keras_ocr.tools.drawAnnotations(image=img, predictions=prediction_groups[0])

    # example of a line mask for the word "Tuesday"
    mask = np.zeros(img.shape[:2], dtype="uint8")
    for box in progress_bar(prediction_groups[0][:10]):
        x0, y0 = box[1][0]
        x1, y1 = box[1][1]
        x2, y2 = box[1][2]
        x3, y3 = box[1][3]

        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)

        thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,
                 thickness)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)

    print('Boxes complete')
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite('text_free_image.jpg', img_rgb)
    return (img)

import pandas as pd
from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp
import threading

def thread_function(data, image_path, directory_path, dim, org):
    blur = cv2.imread(f'{directory_path}{image_path}')
    blur = cv2.resize(blur, dim)
    data.append(
        [image_path, mse(blur, org), rmse(blur, org), psnr(blur, org), uqi(blur, org), msssim(blur, org), ergas(blur, org),
         scc(blur, org), rase(blur, org), sam(blur, org), vifp(blur, org)])

def get_similar_image(reference_image):
    dim = (400, 400)

    ref = cv2.imread(reference_image)
    ref = cv2.resize(ref, dim)

    data = []
    directory_path = '../../../data/Ground Truth/Newspapers/ddd/'
    threads = list()
    for image in progress_bar(os.listdir(directory_path)[:10]):
        if image == reference_image:
            continue
        # while threading.active_count() > 40:
        #     time.sleep(0.01)
        # while psutil.cpu_percent() > 99:
        #     # time.sleep(0.01)
        #     for thread in progress_bar(threads, desc=f"Joining threads:"):
        #         thread.join()
        x = threading.Thread(target=thread_function, args=(data, image, directory_path, dim, ref,))
        x.start()
        threads.append(x)

    for thread in progress_bar(threads, desc='Joining threads:'):
        thread.join()

    columns = ['MSE', 'RMSE', 'PSNR', 'UQI', 'MSSSIM', 'ERGAS', 'SCC', 'RASE', 'SAM', 'VIF']
    df = pd.DataFrame(data,
                      columns=['FILE', 'MSE', 'RMSE', 'PSNR', 'UQI', 'MSSSIM', 'ERGAS', 'SCC', 'RASE', 'SAM', 'VIF'])
    # print(df['SSIM'])
    for column in columns:
        df[column] = df[column] / df[column].abs().max()

    return df



# remove_text2('../../../../../Pictures/TechSmith-Blog-ExtractText.png')
# remove_text('C:\Users\\thoma\Pictures\TechSmith-Blog-ExtractText.png')
reference_image = '../../images/templates/white.jpg'

df = get_similar_image(reference_image)

# get_similar_image('../../../data/Ground Truth/Newspapers/ddd/00530982.tif')
