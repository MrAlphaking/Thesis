import os
import cv2
import numpy as np
from src.utils.Util import progress_bar

class ImageProcessor:
    def __init__(self, save_location):
        self.PAPER_MIN = np.array([16, 30, 30], np.uint8)
        self.PAPER_MAX = np.array([150, 255, 255], np.uint8)
        print("Image processor class created")
        self.save_location = save_location
    def clean_rectangles(self, background_location):
        images = []
        for period in os.listdir(background_location):
            period = f'{background_location}/{period}'

            for file in os.listdir(period):
                file = f'{period}/{file}'
                print(file)

                img = cv2.imread(file)
                hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                frame_threshed = cv2.inRange(hsv_img, self.PAPER_MIN, self.PAPER_MAX)
                mean_value = np.mean(frame_threshed)
                images.append((mean_value, file))

            images.sort(key=lambda x: x[0], reverse=True)
            images = images[5:len(images)]
            for path in images:
                os.remove(path[1])
            print(images)
            images = []




    def find_white_square(self, frame_treshed, image_size):
        highest_value = 0
        x_min = 0
        x_max = image_size

        y_min = 0
        y_max = image_size

        for x in range(0, len(frame_treshed), image_size):
            for y in range(0, len(frame_treshed[x]), image_size):
                if x - len(frame_treshed) > image_size and y - len(frame_treshed[x])     > image_size:
                    mean_value = np.mean(frame_treshed[x:(x + image_size), y:(y+image_size)])
                    if mean_value > highest_value:
                        highest_value = mean_value
                        x_min = x
                        x_max = x + image_size

                        y_min = y
                        y_max = y + image_size
        return x_min, x_max, y_min, y_max

    def create_rectangles(self, image_size, offset_x, offset_y):
        for directory in progress_bar(os.listdir(self.save_location)):
            directory = f'{self.save_location}/{directory}/'

            save_background_location = directory.replace("download", "background")
            if not os.path.exists(save_background_location):
                os.makedirs(directory.replace("download", "background"))

            for file in os.listdir(directory):

                file = f'{directory}{file}'
                # print(file)
                try:
                    img = cv2.imread(file)

                    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                    frame_threshed = cv2.inRange(hsv_img, self.PAPER_MIN, self.PAPER_MAX)
                    # cv2.imwrite('output2.jpg', frame_threshed)


                    # cv2.waitKey(0)
                    file = file.replace("download", "background").replace(".jp2", ".png")
                    x_min, x_max, y_min, y_max = self.find_white_square(frame_threshed, image_size)
                    img = img[x_min:x_max, y_min:y_max]
                    cv2.imwrite(file, img)
                except:
                    print(f"Error with file {file}")



