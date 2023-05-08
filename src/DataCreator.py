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

def create_ocr_from_image_by_dataframe(index, df_list, df, year):
    df = df.loc[df['year'] == year]
    df = df.reset_index(drop=True)

    # img = ImageCreation.create_background(year, 1772, 3000)

    ocr_text = list(df["target"])

    img, text_spacings = ImageCreation.create_image_from_df(0, 1770, ocr_text, year)
    path = f'../images/{index}-{year}.png'
    img.save(path)
    previous_spacing = 0

    ocr_text_list = []
    for spacing in text_spacings:
        cropped_image = img.crop((0, previous_spacing, img.size[0], spacing))
        previous_spacing = spacing
        ocr_text = ocr.get_text(cropped_image)
        ocr_text_list.append(ocr_text)

    df['source'] = ocr_text_list

    df_list.append(df)

def create_ocr_dataframe(df):
    """
    By giving as input a dataframe, this function creates an image per year, and then creates the ocr output for each of the strings.
    :param df:
    :return:
    """

    df.groupby('year')
    years = list(df["year"].unique())
    years.sort()
    # print(years)
    threads = list()
    df_list = list()

    for index, year in enumerate(progress_bar(years, desc='Creating OCR per year')):
        while psutil.cpu_percent() >= 100:
            # print("Sleep")
            time.sleep(0.01)
        x = threading.Thread(target=create_ocr_from_image_by_dataframe, args=(index, df_list, df, year,))
        threads.append(x)
        x.start()

    for thread in progress_bar(threads, desc='Joining thread of creating images: '):
        thread.join()

    df = pd.concat(df_list)
    df.reset_index(drop=True)

    print(df)
    return df
import collections
def equal_distribution_dataframe(df, sample_size=50000):
    print(collections.Counter(list(df['year'])).most_common())
    least_common = collections.Counter(list(df['year'])).most_common()[-1]
    print(least_common[1])
    return df.groupby("year").sample(n=least_common[1], random_state=1)
import numpy as np
def sample_dataframe(df, sample_size):
    # Calculate the number of unique values in the 'year' column
    num_years = df['year'].nunique()

    # Calculate the target sample size for each unique year
    sample_size_per_year = int(np.ceil(sample_size / num_years))

    # Group the DataFrame by the 'year' column
    grouped = df.groupby('year')

    # Sample from each group proportionally to the number of rows in the group
    total_size = 0
    while total_size < sample_size:
        samples = []
        for _, group in grouped:
            n_rows = len(group)
            if n_rows > sample_size_per_year:
                samples.append(group.sample(sample_size_per_year))
            else:
                samples.append(group.sample(n_rows, replace=True))
        total_size = len(pd.concat(samples))
        sample_size_per_year += 1

    print("finished")
    # Combine the samples from each group into a single DataFrame
    sample_df = pd.concat(samples)

    return sample_df

def get_dataframe():
    if READ_FROM_FILE_POST_OCR:
        df = read_pandas(SAVE_PATH_POST_OCR)
        return df

    df = get_data()

    df = clean_dataframe(df)
    print(collections.Counter(list(df['year'])).most_common())
    df = sample_dataframe(df, 50000)
    print(len(df))
    print(df.head())
    print(collections.Counter(list(df['year'])).most_common())
    df = clean_dataframe(df)
    df = create_ocr_dataframe(df)

    if WRITE_FILE_POST_OCR:
        write_pandas(df, SAVE_PATH_POST_OCR)
    return df

# if __name__ == "__main__":
#     df = get_data()
#     df_list = []
#     create_ocr_dataframe(df)