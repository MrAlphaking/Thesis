from src.utils.Util import *
from src.utils.Settings import *

def total_amount_of_words(df):
    str = " ".join(list(df['target'])).replace(',', " ").replace(".", " ").lower().strip()

    print(len(str))

    str = set(" ".join(list(df['target'])).replace(',', " ").replace(".", " ").lower().strip().split(" "))

    print(len(str))



def word_count(df):
    # print(list(df['target']))
    str = " ".join(list(df['target'])).replace(',', " ").replace(".", " ").lower().strip()
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def print_statistics(df_name):
    print(df_name)
    df = read_pandas(f'{BASE_PATH}/dataframes/{df_name}')

    print(word_count(df))
    print(total_amount_of_words(df))

    # print(df.shape)
    # print(df.head())

# print_statistics('PRE_OCR_UNCLEANED_IMPACT')
print_statistics('PRE_OCR_CLEANED_IMPACT')
