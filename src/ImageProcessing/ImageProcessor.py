import os
import cv2
import numpy as np
from src.utils.Util import *
from src.ImageProcessing.ImageCreation import *

class ImageProcessor:

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
    def __init__(self, save_location):
        self.PAPER_MIN = np.array([16, 30, 30], np.uint8)
        self.PAPER_MAX = np.array([150, 255, 255], np.uint8)
        print("Image processor class created")
        self.save_location = save_location

    def create_image_collage(self, background_location):
        """
        This functions creates a single image, intended for creating the image collage in my thesis report.
        :param background_location: The location of the images containing the downloaded background images.
        """

        images = []

        for i in range(10):
            images.append([])
            print(i)
        print(images)
        for period in os.listdir(background_location):
            period = f'{background_location}/{period}'
            for index, file in enumerate(filter(lambda k: '.png' in k, os.listdir(period))):
                # print(index)
                # print(file)
                file = f'{period}/{file}'
                # print(images[index])
                image = Image.open(file)
                images[index].append(image)
        print(images)

        final_image = None

        for row in images:
            horizontal_image = None
            for image in row:
                if horizontal_image is None:
                    horizontal_image = image
                else:
                    horizontal_image = self.get_concat_h(horizontal_image, image)
            if final_image is None:
                final_image = horizontal_image
            else:
                final_image = self.get_concat_v(final_image, horizontal_image)

        # final_image.show()
        final_image.save('latex.png')




    def clean_rectangles(self, background_location, num_images=10):
        """
        This function iterates over the rectangles created, and finds a set number of images to be used as background, based on how much black is in the image.
        :param background_location: The location of the images containing the downloaded background images.
        :param num_images: The amount of images to be saved for background usage.
        """
        images = []
        for period in os.listdir(background_location):
            period = f'{background_location}/{period}'
            for file in os.listdir(period):
                if '.png' in file:
                    file = f'{period}/{file}'
                    img = cv2.imread(file)
                    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    frame_threshed = cv2.inRange(hsv_img, self.PAPER_MIN, self.PAPER_MAX)
                    mean_value = np.mean(frame_threshed)
                    images.append((mean_value, file))
            images.sort(key=lambda x: x[0], reverse=True)
            images = images[num_images:len(images)]
            for path in images:
                os.remove(path[1])
            images = []

    def find_white_square(self, frame_treshed, image_size):
        highest_value = 0
        x_min = 0
        x_max = image_size

        y_min = 0
        y_max = image_size

        for x in range(0, len(frame_treshed), int(image_size / 10)):
            for y in range(0, len(frame_treshed[x]), int(image_size / 10)):

                if x - len(frame_treshed) < image_size and y - len(frame_treshed[x]) < image_size:
                    mean_value = np.sum(frame_treshed[x:(x + image_size), y:(y+image_size)])
                    # print(mean_value)
                    if mean_value > highest_value:
                        # print(mean_value)
                        highest_value = mean_value
                        x_min = x
                        x_max = x + image_size

                        y_min = y
                        y_max = y + image_size
        return x_min, x_max, y_min, y_max

    def test(self):
        for directory in progress_bar(os.listdir(self.save_location)):
            directory = f'{self.save_location}/{directory}/'
            for file in os.listdir(directory):
                file = f'{directory}{file}'
                try:
                    img = cv2.imread(file)
                    print(img.shape)
                except:
                    print("")

    def create_rectangles(self, image_size, offset_x, offset_y):
        for directory in progress_bar(os.listdir(self.save_location)):
            # if '1700-1710' not in directory:
            #     continue
            print(directory)
            directory = f'{self.save_location}/{directory}/'
            print(directory)
            save_background_location = directory.replace("download", "background")
            if not os.path.exists(save_background_location):
                os.makedirs(directory.replace("download", "background"))

            save_treshold_location = directory.replace("download", "treshold")
            if not os.path.exists(save_treshold_location):
                os.makedirs(directory.replace("download", "treshold"))

            for file in os.listdir(directory):
                file = f'{directory}{file}'
                try:
                    print(file)
                    img = cv2.imread(file)

                    # cv2.imwrite('../images/frame_treshold_no_filter.png', img)
                    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                    frame_threshed = cv2.inRange(hsv_img, self.PAPER_MIN, self .PAPER_MAX)
                    # file_treshold = file.replace("download", "treshold").replace(".jp2", ".png")
                    # cv2.imwrite('../images/frame_treshold.png', frame_threshed)
                    file = file.replace("download", "background").replace(".jp2", ".png")
                    # cv2.imwrite(file_treshold, frame_threshed)
                    # print(file_treshold)

                    x_min, x_max, y_min, y_max = self.find_white_square(frame_threshed, image_size)
                    img = img[x_min:x_max, y_min:y_max]
                    cv2.imwrite(file, img)
                except:
                    print_telegram(f"Error with file {file}")



