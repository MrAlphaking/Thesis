from data_loader.DataLoader import *
from OCR import *
from src.ImageProcessing.ImageCreation import *

ImageCreation = ImageCreation()
ocr = OCR()

def get_dataframe():
    if READ_FROM_FILE_POST_OCR:
        df = read_pandas(SAVE_PATH_POST_OCR)
        return df

    df = get_data()
    print(df.head())

    # print(list(df['target']))
    image_list = ImageCreation.create_image_list(df)
    ocr_list = ocr.get_ocr_list(image_list)
    df['source'] = ocr_list
    ImageCreation.remove_image_list(image_list)

    if WRITE_FILE_POST_OCR:
        write_pandas(df, SAVE_PATH_POST_OCR)
    return df
