import pandas as pd

from data_loader.DataLoader import *
from OCR import *
from src.ImageProcessing.ImageCreation import *

ImageCreation = ImageCreation()
ocr = OCR()
def save_df(index, source_text_list, threads, df):
    if index % 10000 == 0 and index != 0:
        for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID,
                           desc="Joining threads of creating images: "):
            thread.join()
        temp_df = df.copy()
        temp_df = temp_df.head(index)
        print_telegram(f'Saving dataframe at index {index}')
        source_text_list.sort(key=lambda x: x[0])
        temp_df['source'] = list(zip(*source_text_list))[1]
        print(temp_df.head())

        write_pandas(temp_df, f'{SAVE_PATH_POST_OCR}_{index}')
def create_ocr_from_image(index, source_text_list, target_text, year):
    image = ImageCreation.create_image2(index, target_text, year)
    ocr_text = ocr.get_text(image)
    # print(f'Source: {ocr_text}\nTarget: {target_text}')
    source_text_list.append((index, ocr_text))

def create_ocr_dataframe2(df):
    source_text_list = []
    threads = list()

    for index, row in tqdm(df.iterrows(), token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID,
                           desc="Creating text from images: "):
        # images.append((index, self.create_image(text, index=index)))
        while psutil.cpu_percent() >= 100:
            # print("Sleep")
            time.sleep(0.01)

        save_df(index, source_text_list, threads, df)

        x = threading.Thread(target=create_ocr_from_image,
                             args=(index, source_text_list, row['target'], row['year'],))
        threads.append(x)
        x.start()

    for thread in tqdm(threads, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID,
                       desc="Joining threads of creating images: "):
        thread.join()
    source_text_list.sort(key=lambda x: x[0])
    df['source'] = list(zip(*source_text_list))[1]
    # df['source'] = source_text_list
    return df

def create_ocr_from_image_by_dataframe(index, df):



    df.groupby('year')
    years = list(df["year"].unique())
    print(years)

    year = 1650
    df = df.loc[df['year'] == year]
    df = df.reset_index(drop=True)

    img = ImageCreation.create_background(year, 1772, 3000)
    # img.show()

    ocr_text = list(df["target"])
    print(df)

    ImageCreation.create_image_from_df(0, img, 1770, 3000, ocr_text, 1650)

    # image = ImageCreation.create_image2(index, target_text, year)
    # ocr_text = ocr.get_text(image)
    # print(f'Source: {ocr_text}\nTarget: {target_text}')
    # source_text_list.append((index, ocr_text))


def create_ocr_dataframe(df):
    df.groupby('year')
    years = list(df["year"].unique())
    print(years)
    source_text_list = []
    threads = list()

    for index, year in enumerate(progress_bar(years, desc='Creating OCR per year')):
        while psutil.cpu_percent() >= 100:
            # print("Sleep")
            time.sleep(0.01)
        x = threading.Thread(target=create_ocr_from_image_by_dataframe, args=(index, df.loc[df['year'] == year],))
        threads.append(x)
        x.start()

    for thread in progress_bar(threads, desc='Joining thread of creating images: '):
        thread.join()
    # source_text_list.sort(key=lambda x: x[0])
    # df['source'] = list(zip(*source_text_list))[1]
    # df['source'] = source_text_list
    return df

def get_dataframe():
    if READ_FROM_FILE_POST_OCR:
        df = read_pandas(SAVE_PATH_POST_OCR)
        return df

    df = get_data()
    # df = df.iloc[121000:122000]

    print(df.head())

    df = create_ocr_dataframe(df)

    # print(list(df['target']))
    # image_list = ImageCreation.create_image_list(df)
    # ocr_list = ocr.get_ocr_list(image_list)
    # df['source'] = ocr_list
    # ImageCreation.remove_image_list(image_list)

    if WRITE_FILE_POST_OCR:
        write_pandas(df, SAVE_PATH_POST_OCR)
    return df

if __name__ == "__main__":
    df = get_data()

    create_ocr_from_image_by_dataframe(0, df)
    # temp_list = []
    # create_ocr_from_image(0, temp_list, "Haar onderwerp is intusschen voor ons vaderland zoo allergewigtigst, dat men bijna geregtigd kan zijn tot de vraag, of niet veeleer de orde van behandeling behoorde te worden omgekeerd", 1650)
    # print(temp_list)
