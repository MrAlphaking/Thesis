import collections
class TextStatistics:
    def __init__(self):
        print("Statistic class created")

    def print_wordcount(self, sentences):
        words_counter = collections.Counter([word for sentence in sentences for word in sentence.split()])

        print('{} Words.'.format(len([word for sentence in sentences for word in sentence.split()])))
        print('{} unique words.'.format(len(words_counter)))
        print('30 Most common words in the dataset:')
        print('"' + '" "'.join(list(zip(*words_counter.most_common(30)))[0]) + '"')
