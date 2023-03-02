from data_loader.DataLoader import *
from OCR import *
from src.ImageProcessing.ImageCreation import *

ImageCreation = ImageCreation()
ocr = OCR()

def add_ocr_text(index, row, sources):
    target = row['target']
    output_path = ImageCreation.getImage(target, index=index)
    source = (index, ocr.get_ocr(output_path).strip("\n"))
    sources.append(source)
    # os.remove(output_path)

def get_dataframe():

    df = get_data()
    image_list = ImageCreation.create_image_list(list(df['target']))
    ocr_list = ocr.get_ocr_list2(image_list)
    ImageCreation.remove_image_list(image_list)

get_dataframe()
# def get_dataframe():
#     if READ_FROM_FILE_POST_OCR:
#         df = read_pandas(SAVE_PATH_POST_OCR)
#         return df
#
#     df = get_data()
#
#     # statistics = TextStatistics()
#     sources = []
#     threads = list()
#     for index, row in tqdm(df.iterrows(), total=df.shape[0], desc='Processing OCR images', token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID):
#         if index % 10000 == 0 and index != 0 and WRITE_FILE_POST_OCR:
#             for thread in threads:
#                 thread.join()
#             df_copy = df.copy()
#             df_copy = df_copy.head(index)
#             sources_temp = sources.copy()
#             sources_temp.sort(key=lambda x: x[0])
#             df_copy['source'] = list(zip(*sources_temp))[1]
#             write_pandas(df_copy, SAVE_PATH_POST_OCR + f"_temp_until_{index}")
#             threads = list()
#         while threading.active_count() > MAX_THREADING_COUNT:
#             time.sleep(0.1)
#
#         x = threading.Thread(target=add_ocr_text, args=(index, row, sources,))
#         threads.append(x)
#         x.start()
#
#     for thread in tqdm(threads, desc="joining threads"):
#         thread.join()
#
#     sources.sort(key=lambda x: x[0])
#     print_telegram(sources)
#
#     sources = list(zip(*sources))[1]
#
#     df['source'] = sources
#
#     if WRITE_FILE_POST_OCR:
#         write_pandas(df, SAVE_PATH_POST_OCR)
#
#     return df
