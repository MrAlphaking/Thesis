import torch

BASE_PATH = '../../data/Ground Truth/'
#BASE_PATH = '/media/sf_GitHub/data/Ground Truth/'

# DataLoader.py
READ_FROM_FILE_PRE_OCR = True
READ_FROM_FILE_POST_OCR = False
READ_FROM_FILE_INTERMEDIATES = True
WRITE_FILE_POST_OCR = True
WRITE_FILE_PRE_OCR_UNCLEANED = True
WRITE_FILE_PRE_OCR_CLEANED = True

SAVE_PATH_17THCENTURYNEWSPAPER = BASE_PATH + "dataframes/17THCENTURYNEWSPAPER"
SAVE_PATH_HISTORICALNEWSPAPERS = BASE_PATH + "dataframes/HISTORICALNEWSPAPER"
SAVE_PATH_DBNL_BOOKS = BASE_PATH + "dataframes/DBNL_BOOKS"
SAVE_PATH_STATENVERTALING = BASE_PATH + "dataframes/STATENVERTALING"

SAVE_PATH_IMPACT = BASE_PATH + "dataframes/IMPACT_"

# DataCreator.py
# MAX_THREADING_COUNT = 50
SAVE_PATH_POST_OCR = BASE_PATH + "dataframes/POST_OCR_17th"
SAVE_PATH_PRE_OCR_UNCLEANED = BASE_PATH + "dataframes/PRE_OCR_UNCLEANED_17th"
SAVE_PATH_PRE_OCR_CLEANED = BASE_PATH + "dataframes/PRE_OCR_CLEANED_17th"

# Telegram

TELEGRAM_BOOLEAN = False
TELEGRAM_TOKEN = "6148002997:AAGOq31lNenxEf9PvFWsNTHcf6t7UcoUsZ8"
TELEGRAM_CHAT_ID = "6198204545"

# T5Model

NUMBER_OF_EPOCHS = 5
TENSOR_DTYPE = torch.long

DATASET_SIZE = 50000
MODEL_SAVE_FOLDER = f'models/'

# Delpher

delpher_api_key = 'dd69d73d-91c0-43a5-8516-2ccf458a158a'
SAVE_PATH_DOWNLOAD_IMAGE = '../images/download'
SAVE_PATH_BACKGROUND_IMAGE = '../images/background'