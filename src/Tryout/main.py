import os

from keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils import pad_sequences

from keras.models import Model
from keras.layers import GRU, Input, Dense, TimeDistributed, Activation, RepeatVector, Bidirectional
from tensorflow.keras.layers import Embedding
from keras.optimizers import Adam
from keras.losses import sparse_categorical_crossentropy

import collections
import numpy as np

def load_data(path):
    """
    Load dataset
    """
    input_file = os.path.join(path)
    with open(input_file, "r") as f:
        data = f.read()

    return data.split('\n')

def pad(x, length=None):
    """
    Pad x
    :param x: List of sequences.
    :param length: Length to pad the sequence to.  If None, use length of longest sequence in x.
    :return: Padded numpy array of sequences
    """
    # TODO: Implement
    if length is None:
        length = max([len(sentence) for sentence in x])
    return pad_sequences(x, maxlen = length, padding = 'post')

def preprocess(x, y):
    """
    Preprocess x and y
    :param x: Feature List of sentences
    :param y: Label List of sentences
    :return: Tuple of (Preprocessed x, Preprocessed y, x tokenizer, y tokenizer)
    """
    preprocess_x, x_tk = tokenize(x)
    preprocess_y, y_tk = tokenize(y)

    preprocess_x = pad(preprocess_x)
    preprocess_y = pad(preprocess_y)

    # Keras's sparse_categorical_crossentropy function requires the labels to be in 3 dimensions
    preprocess_y = preprocess_y.reshape(*preprocess_y.shape, 1)

    return preprocess_x, preprocess_y, x_tk, y_tk

def tokenize(x):
    """
    Tokenize x
    :param x: List of sentences/strings to be tokenized
    :return: Tuple of (tokenized x data, tokenizer used to tokenize x)
    """
    # TODO: Implement
    x_tk = Tokenizer(char_level=False)
    x_tk.fit_on_texts(x)
    return x_tk.texts_to_sequences(x), x_tk


def simple_model(input_shape, output_sequence_length, english_vocab_size, french_vocab_size):
    """
    Build and train a basic RNN on x and y
    :param input_shape: Tuple of input shape
    :param output_sequence_length: Length of output sequence
    :param english_vocab_size: Number of unique English words in the dataset
    :param french_vocab_size: Number of unique French words in the dataset
    :return: Keras model built, but not trained
    """
    # TODO: Build the layers
    learning_rate = 1e-3
    input_seq = Input(input_shape[1:])
    rnn = GRU(64, return_sequences=True)(input_seq)
    logits = TimeDistributed(Dense(french_vocab_size))(rnn)
    model = Model(input_seq, Activation('softmax')(logits))
    model.compile(loss=sparse_categorical_crossentropy,
                  optimizer=Adam(learning_rate),
                  metrics=['accuracy'])

    return model

def logits_to_text(logits, tokenizer):
    """
    Turn logits from a neural network into text using the tokenizer
    :param logits: Logits from a neural network
    :param tokenizer: Keras Tokenizer fit on the labels
    :return: String that represents the text of the logits
    """
    index_to_words = {id: word for word, id in tokenizer.word_index.items()}
    index_to_words[0] = ''

    return ' '.join([index_to_words[prediction] for prediction in np.argmax(logits, 1)])


if __name__ == '__main__':
    english_sentences = load_data('../data/small_vocab_en')
    french_sentences = load_data('../data/small_vocab_fr')

    print('Dataset Loaded')

    for sample_i in range(2):
        print('small_vocab_en Line {}:  {}'.format(sample_i + 1, english_sentences[sample_i]))
        print('small_vocab_fr Line {}:  {}'.format(sample_i + 1, french_sentences[sample_i]))

    english_words_counter = collections.Counter([word for sentence in english_sentences for word in sentence.split()])
    french_words_counter = collections.Counter([word for sentence in french_sentences for word in sentence.split()])

    print('{} English words.'.format(len([word for sentence in english_sentences for word in sentence.split()])))
    print('{} unique English words.'.format(len(english_words_counter)))
    print('10 Most common words in the English dataset:')
    print('"' + '" "'.join(list(zip(*english_words_counter.most_common(10)))[0]) + '"')
    print()
    print('{} French words.'.format(len([word for sentence in french_sentences for word in sentence.split()])))
    print('{} unique French words.'.format(len(french_words_counter)))
    print('10 Most common words in the French dataset:')
    print('"' + '" "'.join(list(zip(*french_words_counter.most_common(10)))[0]) + '"')

    # Tokenize Example output
    text_sentences = [
        'The quick brown fox jumps over the lazy dog .',
        'By Jove , my quick study of lexicography won a prize .',
        'This is a short sentence .']
    text_tokenized, text_tokenizer = tokenize(text_sentences)
    print(text_tokenizer.word_index)
    print()
    for sample_i, (sent, token_sent) in enumerate(zip(text_sentences, text_tokenized)):
        print('Sequence {} in x'.format(sample_i + 1))
        print('  Input:  {}'.format(sent))
        print('  Output: {}'.format(token_sent))

    # tests.test_pad(pad)

    # Pad Tokenized output
    test_pad = pad(text_tokenized)
    for sample_i, (token_sent, pad_sent) in enumerate(zip(text_tokenized, test_pad)):
        print('Sequence {} in x'.format(sample_i + 1))
        print('  Input:  {}'.format(np.array(token_sent)))
        print('  Output: {}'.format(pad_sent))

    preproc_english_sentences, preproc_french_sentences, english_tokenizer, french_tokenizer = \
        preprocess(english_sentences, french_sentences)

    max_english_sequence_length = preproc_english_sentences.shape[1]
    max_french_sequence_length = preproc_french_sentences.shape[1]
    english_vocab_size = len(english_tokenizer.word_index)
    french_vocab_size = len(french_tokenizer.word_index)

    print('Data Preprocessed')
    print("Max English sentence length:", max_english_sequence_length)
    print("Max French sentence length:", max_french_sequence_length)
    print("English vocabulary size:", english_vocab_size)
    print("French vocabulary size:", french_vocab_size)



    print('`logits_to_text` function loaded.')

    # tests.test_simple_model(simple_model)

    # Reshaping the input to work with a basic RNN
    tmp_x = pad(preproc_english_sentences, max_french_sequence_length)
    tmp_x = tmp_x.reshape((-1, preproc_french_sentences.shape[-2], 1))

    # Train the neural network
    simple_rnn_model = simple_model(
        tmp_x.shape,
        max_french_sequence_length,
        english_vocab_size,
        french_vocab_size)
    simple_rnn_model.fit(tmp_x, preproc_french_sentences, batch_size=1024, epochs=10, validation_split=0.2)

    # Print prediction(s)
    print(logits_to_text(simple_rnn_model.predict(tmp_x[:1])[0], french_tokenizer))