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
    return avg_wer, avg_cer, avg_jaccard

def plot1(df):
    """
    prints the amount of sentences in the total vocabulary per year
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
    for sentence in input_text:
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

import random
def count_distinct_words(word_set, string):

    for word in str(string).split(" "):
        word = word.replace("[^A-Za-z0-9]", "")
        words = word.split()
        word_set.update(words)
    return word_set

def count_distinctive_words_list(sentence_list):
    word_set = set()
    for sentence in sentence_list:
        word_set = count_distinct_words(word_set, sentence)

    return len(word_set)

def set_number_of_words(string_list, num_of_words=1000):
    word_set_ground_truth = set()
    word_set_ocr = set()
    return_list = []
    for row in string_list:
        if len(row[0]) > 128:
            continue
        word_set_ground_truth = count_distinct_words(word_set_ground_truth, row[0])
        word_set_ocr = count_distinct_words(word_set_ocr, row[1])
        return_list.append(row[1])
        if len(word_set_ground_truth) >= num_of_words:
            return len(word_set_ground_truth), len(word_set_ocr), return_list

    return len(word_set_ground_truth), len(word_set_ocr), return_list

def print_list(sentence_list, message =""):
    print(f'{message}')
    for sentence in sentence_list:
        print(sentence)
def print_graph_equal_words_per_year():
    x_tick_label = get_xticklabels()
    df = read_pandas(f'{BASE_PATH}/dataframes/TOTAL_USED_DATASET_200000')
    from sklearn.utils import shuffle
    df = shuffle(df)
    tokenizer = AutoTokenizer.from_pretrained("./models/google-flan-t5-base-TOTALAttempt2-post-correction-200000")
    model = AutoModelForSeq2SeqLM.from_pretrained("./models/google-flan-t5-base-TOTALAttempt2-post-correction-200000")

    string_list_ground_truth = []
    string_list_ocr = []
    string_list_post_corrected = []

    for label in progress_bar(x_tick_label):
        print(label)
        label_split = label.split('-')
        mask = (df['year'] > int(label_split[0])) & (df['year'] <= int(label_split[1]))
        df_temp = df.loc[mask]

        ground_truth = list(df_temp['target'])
        pre_correction = list(df_temp['source'])

        word_set_ground_truth_length, word_set_ocr_length, sentence_list = set_number_of_words(zip(ground_truth, pre_correction), num_of_words=2000)

        word_set_post_corrected_length = count_distinctive_words_list(post_correct_list(sentence_list, model, tokenizer))
        # print(x_tick_label)
        # print(label)
        # print(x_tick_label[label])
        # print(word_set_ground_truth_length)
        # print(label)
        string_list_ground_truth.append(f'({x_tick_label[label]}, {word_set_ground_truth_length}) %{label}')
        string_list_ocr.append(f'({x_tick_label[label]}, {word_set_ocr_length}) %{label}')
        string_list_post_corrected.append(f'({x_tick_label[label]}, {word_set_post_corrected_length}) %{label}')

        print_list(string_list_ground_truth, message='ground truth')
        print_list(string_list_ocr, message='ocr')
        print_list(string_list_post_corrected, message='post_corrected')

        # post_correction = list(df['source'])

def equal_distribution_dataframe(df):
    least_common = collections.Counter(list(df['year'])).most_common()[-1]
    print(least_common[1])
    return df.groupby("year").sample(n=least_common[1], random_state=1)
def print_statistics():
    # df_names = ['PRE_OCR_CLEANED_statenvertaling', 'PRE_OCR_CLEANED_IMPACT', 'PRE_OCR_CLEANED_historical', 'PRE_OCR_CLEANED_DBNL', 'PRE_OCR_CLEANED_17th']
    df_names = ['PRE_OCR_CLEANED']
    for df_name in df_names:
        print(df_name)
        df = read_pandas(f'{BASE_PATH}/dataframes/{df_name}')

        # df = equal_distribution_dataframe(df)
        print(len(df))

        plot1(df)
        plot2(df)
import sys

def perform_performance_comparison_total():
    directory1 = f'./models/total/'
    model_names = os.listdir(directory1)

    df = read_pandas('../../data/Ground Truth/dataframes/TOTAL_TEST_DATASET_500')

    for model_name in model_names:
        # output_string_post = f'& {model_name} '
        # output_string_normal = f'& Baseline'
        print(model_name)

        tokenizer = AutoTokenizer.from_pretrained(f"./models/total/{model_name}")
        model = AutoModelForSeq2SeqLM.from_pretrained(f"./models/total/{model_name}")

        source = list(df['source'])
        # print(f'{model_variant}/{model_name} on dataset: {df_name}')

        post_corrected_source = post_correct_list(source, model, tokenizer)
        target = list(df['target'])
        # print(f'Normal: {wer_cer_jaccard(source, target)}')
        avg_wer, avg_cer, avg_jaccard = wer_cer_jaccard(post_corrected_source, target)
        print('Post-corrected')
        print(f'WER: {round(avg_wer, 3)} \\newline CER: {round(avg_cer, 3)} \\newline Jaccard: {round(avg_jaccard, 3)}')
        
        print('Baseline')
        avg_wer, avg_cer, avg_jaccard = wer_cer_jaccard(source, target)
        print(f'WER: {round(avg_wer, 3)} \\newline CER: {round(avg_cer, 3)} \\newline Jaccard: {round(avg_jaccard, 3)}')

def perform_performance_comparison(model_variant):
    print_telegram("Starting creating evaluation tables")
    directory1 = f'./models/{model_variant}/'
    model_names = os.listdir(directory1)
    print(model_names)
    directory2 = '../../data/Ground Truth/dataframes/post'
    df_names = os.listdir(directory2)
    print_bool = True
    for model_name in model_names:
        output_string_post = f'& {model_name} '
        output_string_normal = f'& Baseline'

        tokenizer = AutoTokenizer.from_pretrained(f"./models/{model_variant}/{model_name}")
        model = AutoModelForSeq2SeqLM.from_pretrained(f"./models/{model_variant}/{model_name}")
        for df_name in df_names:
            df = read_pandas(f'{directory2}/{df_name}')

            # write_pandas(df, f'../../data/Ground Truth/dataframes/post/{df_name}-250')

            source = list(df['source'])
            # print(f'{model_variant}/{model_name} on dataset: {df_name}')

            post_corrected_source = post_correct_list(source, model, tokenizer)
            target = list(df['target'])
            # print(f'Normal: {wer_cer_jaccard(source, target)}')
            avg_wer, avg_cer, avg_jaccard = wer_cer_jaccard(post_corrected_source, target)
            output_string_post += f' & WER: {round(avg_wer, 3)} \\newline CER: {round(avg_cer, 3)} \\newline Jaccard: {round(avg_jaccard, 3)}'

            avg_wer, avg_cer, avg_jaccard = wer_cer_jaccard(source, target)
            output_string_normal += f' & WER: {round(avg_wer, 3)} \\newline CER: {round(avg_cer, 3)} \\newline Jaccard: {round(avg_jaccard, 3)}'

            # print(f'Post-corrected: {wer_cer_jaccard(post_corrected_source, target)}')
            # print(wer_cer_jaccard(post_corrected_source, target))

        output_string_post += '\\\\ \cline{2 - 7}'
        output_string_normal += '\\\\ \cline{2 - 7}'
        if print_bool:
            with open(f'output-{model_variant}.txt', 'a') as f:
                f.write(f'{output_string_normal}\n')
            print_telegram(output_string_normal)
            print_bool = False

        with open(f'output-{model_variant}.txt', 'a') as f:
            f.write(f'{output_string_post}\n')
        print_telegram(output_string_post)
    print_telegram(f"Finished evaluation for {model_variant}")



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
# print_graph_equal_words_per_year()
# perform_performance_comparison('google')
perform_performance_comparison_total()
# perform_performance_comparison('yhavinga')
# perform_performance_comparison_ICDAR()
