import os
from collections import Counter
from data_loader.DataLoader import *
from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModelForSeq2SeqLM
# df = get_data()
import collections
import Levenshtein


def get_xticklabels():
    xticklabels = ["1610-1619", "1620-1629", "1630-1639", "1640-1649", "1650-1659", "1660-1669", "1670-1679",
                   "1680-1689", "1690-1699", "1700-1709", "1710-1719", "1720-1729", "1730-1739", "1740-1749",
                   "1750-1759", "1760-1769", "1770-1779", "1780-1789", "1790-1799", "1800-1809", "1810-1819",
                   "1820-1829", "1830-1839", "1840-1849", "1850-1859", "1860-1869", "1870-1879", "1880-1889",
                   "1890-1899", "1900-1909", "1910-1919", "1920-1929", "1930-1939", "1940-1949", "1950-1959",
                   "1960-1969", "1970-1979", "1980-1989", "1990-1999"]

    xtick_dict = {}
    for i in range(len(xticklabels)):
        xtick_dict[xticklabels[i]] = i
    return xtick_dict


import pandas as pd
import Levenshtein

def update_set(string_list, words_set):

    for word in string_list:
        words_set.add(word.replace(",", "").replace(".", ""))


def wer_cer_jaccard(pred_list, truth_list):
    wer_scores = []
    cer_scores = []
    jaccard_scores = []
    pred_words_set = set()
    truth_words_set = set()
    for i in range(len(pred_list)):
        pred = str(pred_list[i])
        truth = str(truth_list[i])
        # print(pred)
        # Word Error Rate (WER)
        pred_words = pred.split()
        truth_words = truth.split()

        update_set(pred_words, pred_words_set)
        update_set(truth_words, truth_words_set)


        wer = float(Levenshtein.distance(pred_words, truth_words)) / len(truth_words)

        # Character Error Rate (CER)
        pred_chars = list(pred)
        truth_chars = list(truth)
        cer = float(Levenshtein.distance(pred_chars, truth_chars)) / len(truth_chars)

        # Jaccard Index
        pred_set = set(pred_words)
        truth_set = set(truth_words)
        jaccard = len(pred_set.intersection(truth_set)) / len(pred_set.union(truth_set))

        wer_scores.append(wer)
        cer_scores.append(cer)
        jaccard_scores.append(jaccard)

    avg_wer = sum(wer_scores) / len(wer_scores)
    avg_cer = sum(cer_scores) / len(cer_scores)
    avg_jaccard = sum(jaccard_scores) / len(jaccard_scores)
    return avg_wer, avg_cer, avg_jaccard, len(pred_words_set), len(truth_words_set)

# def plot1(df):
#     """
#     prints the total amount of sentences per time period
#     :param df: The df that contains the sentences
#     """
#     print("Plot 1 Sentences")
#     xtick_dict = get_xticklabels()
#     years = list(df['year'])
#     years.sort()
#     # print(count[years[0]])
#     freq = Counter()
#     for x in years:
#         freq[(x - 1) // 10] += 1
#     # print(freq.values())
#     # print(freq.keys())
#
#     for index, key in enumerate(freq.keys()):
#         print(f'({xtick_dict[f"{key}0-{key}9"]}, {freq[key]}) %{key}0-{key}9')

def plot1(df):
    """
    prints the amount of words in the total vocabulary per year
    :param df: The df that contains the sentences
    """
    print("Plot 1 Sentences")
    years = list(set(df['year']))
    years.sort()
    # print(df)
    max = 0
    for year in years:
        df_temp = df[df['year'] == int(year)]
        df_temp.reset_index(drop=True)
        target_texts = list(df_temp['target'])

        amount_of_sentences = len(target_texts)
        if amount_of_sentences > max:
            max = amount_of_sentences
        print(f'({year}, {amount_of_sentences})')

    print(f'max value = {max}')
def plot2(df):
    """
    prints the amount of words in the total vocabulary per year
    :param df: The df that contains the sentences
    """
    print("Plot 2 Words")
    years = list(set(df['year']))
    years.sort()
    # print(df)
    max = 0
    for year in years:
        df_temp = df[df['year'] == int(year)]
        df_temp.reset_index(drop=True)
        target_texts = list(df_temp['target'])

        target_texts = set(" ".join(target_texts).replace(',', " ").replace(".", " ").lower().strip().split(" "))
        # target_texts = " ".join(target_texts).lower().strip().split(" ")
        # print(f'before: {len(target_texts)}')
        # target_texts = set(target_texts)
        # print(f'After: {len(target_texts)}')

        amount_of_words = len(set(target_texts))
        if amount_of_words > max:
            max = amount_of_words
        print(f'({year}, {amount_of_words})')

    print(f'max value = {max}')

# tokenizer = AutoTokenizer.from_pretrained("./models/yhavinga-t5-base-dutch-post-correction-50000-IMPACT")
# model = AutoModelWithLMHead.from_pretrained("./models/yhavinga-t5-base-dutch-post-correction-50000-IMPACT")
# tokenizer = AutoTokenizer.from_pretrained("../models/google-flan-t5-base-post-correction-140000")
# model = AutoModelWithLMHead.from_pretrained("../models/google-flan-t5-base-post-correction-140000")
task_prefix = 'post-correction: '
delpher = Delpher()


def post_correct(input_text, model, tokenizer):
    input_text = str(input_text)
    input_text = task_prefix + input_text + "</s>"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=256, num_beams=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

def post_correct_list(input_text, model, tokenizer):
    return_list = []
    for sentence in progress_bar(input_text):
        return_list.append(post_correct(sentence, model, tokenizer))
    return return_list

def sample_dataframe(df, sample_size):
    # Calculate the number of unique values in the 'year' column
    num_years = df['year'].nunique()

    # Calculate the target sample size for each unique year
    sample_size_per_year = int(np.ceil(sample_size / num_years))

    # Group the DataFrame by the 'year' column
    grouped = df.groupby('year')

    # Sample from each group proportionally to the number of rows in the group
    samples = []
    for _, group in grouped:
        n_rows = len(group)
        if n_rows > sample_size_per_year:
            samples.append(group.sample(sample_size_per_year))
        else:
            samples.append(group.sample(n_rows, replace=True))

    # Combine the samples from each group into a single DataFrame
    sample_df = pd.concat(samples)

    # Trim the sample to the desired sample size
    sample_df = sample_df.sample(sample_size)

    return sample_df
def equal_distribution_dataframe(df):
    least_common = collections.Counter(list(df['year'])).most_common()[-1]
    print(least_common[1])
    return df.groupby("year").sample(n=least_common[1], random_state=1)
def print_statistics():
    df_names = ['PRE_OCR_CLEANED_statenvertaling', 'PRE_OCR_CLEANED_IMPACT', 'PRE_OCR_CLEANED_historical', 'PRE_OCR_CLEANED_DBNL', 'PRE_OCR_CLEANED_17th']
    for df_name in df_names:
        print(df_name)
        df = read_pandas(f'{BASE_PATH}/dataframes/{df_name}')

        df = equal_distribution_dataframe(df)
        print(len(df))

        # plot1(df)
        # plot2(df)

def perform_performance_comparison():
    df_names = ['POST_OCR_IMPACT']
    model_names = ['IMPACT']
    model_variants = ['google-flan-t5-base-post-correction-50000-', 'yhavinga-t5-base-dutch-post-correction-50000-']
    for df_name in df_names:
        df = read_pandas(f'{BASE_PATH}/dataframes/{df_name}').sample(100)
        source = list(df['source'])
        for model_name in model_names:
            for model_variant in model_variants:
                print(f'{model_variant}{model_name} on dataset: {df_name}')
                tokenizer = AutoTokenizer.from_pretrained(f"./models/{model_variant}{model_name}")
                model = AutoModelForSeq2SeqLM.from_pretrained(f"./models/{model_variant}{model_name}")
                post_corrected_source = post_correct_list(source, model, tokenizer)
                target = list(df['target'])
                print(f'Normal: {wer_cer_jaccard(source, target)}')
                print(f'Post-corrected: {wer_cer_jaccard(post_corrected_source, target)}')
                # print(wer_cer_jaccard(post_corrected_source, target))

def perform_performance_comparison_ICDAR():
    directory = '../../data/Ground Truth/ICDAR'
    files = os.listdir(directory)
    icdar_ocr_string = "[OCR_toInput] "
    icdar_ground_truth_string = "[ GS_aligned] "

    icdar_ground_truth = []
    icdar_ocr_pre = []
    for file in files:
        file = f'{directory}/{file}'
        f = open(file, "r", encoding='utf8')
        for line in f:
            line = line.replace('\n', '').replace('@','')
            if icdar_ocr_string in line:
                icdar_ocr_pre.append(line.replace(icdar_ocr_string,''))
            if icdar_ground_truth_string in line:
                icdar_ground_truth.append(line.replace(icdar_ground_truth_string,''))


    directory = './models'
    model_names = os.listdir(directory)
    print(files)

    for model_name in model_names:
        print(f'{model_name} on dataset: ICDAR')
        tokenizer = AutoTokenizer.from_pretrained(f"{directory}/{model_name}")
        model = AutoModelForSeq2SeqLM.from_pretrained(f"{directory}/{model_name}")
        icdar_ocr_post = []

        for line in progress_bar(icdar_ocr_pre[:1]):
            icdar_ocr_post.append(" ".join(post_correct_list(line.split('.')), model, tokenizer))
        print(f'Normal: {wer_cer_jaccard(icdar_ocr_pre, icdar_ground_truth)}')
        print(f'Post-corrected: {wer_cer_jaccard(icdar_ocr_post, icdar_ground_truth)}')
# print_statistics()
# perform_performance_comparison()
perform_performance_comparison_ICDAR()
