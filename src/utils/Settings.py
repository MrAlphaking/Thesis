import torch

BASE_PATH = '../../data/Ground Truth/'
#BASE_PATH = '/media/sf_GitHub/data/Ground Truth/'

# DataCleaner.py
READ_FROM_FILE_PRE_OCR = True
READ_FROM_FILE_INTERMEDIATES = True
WRITE_FILE_PRE_OCR = False
SAVE_PATH_PRE_OCR = BASE_PATH + "dataframes/PRE_OCR"
SAVE_PATH_17THCENTURYNEWSPAPER = BASE_PATH + "dataframes/17THCENTURYNEWSPAPER"
SAVE_PATH_HISTORICALNEWSPAPERS = BASE_PATH + "dataframes/HISTORICALNEWSPAPER"
SAVE_PATH_DBNL_BOOKS = BASE_PATH + "dataframes/DBNL_BOOKS"

# DataCreator.py
MAX_THREADING_COUNT = 20
READ_FROM_FILE_POST_OCR = True
WRITE_FILE_POST_OCR = False
SAVE_PATH_POST_OCR = BASE_PATH + "dataframes/POST_OCR_temp_until_270000"

# ImageCreation.py
IMAGE_PATH_BLANK = "../images/templates/white.jpg"
IMAGE_WRITE_BLANK = "../images/run/white-edited-"

# Telegram

TELEGRAM_TOKEN = "6148002997:AAGOq31lNenxEf9PvFWsNTHcf6t7UcoUsZ8"
TELEGRAM_CHAT_ID = "6198204545"

# T5Model

NUMBER_OF_EPOCHS = 1
TENSOR_DTYPE = torch.long

DATASET_SIZE = 10
MODEL_SAVE_FOLDER = f'models/t5-base-dutch-post-correction-{DATASET_SIZE}'
