import os
import re
from pathlib import Path
from TextExtractor import TextExtractor
from TextStatistics import TextStatistics
import phunspell

# import neuspell
# from neuspell import BertChecker

sentences = ["De kat wil wel vis eten maar geen poot nat maken."]

# Spelling corrector not including dutch:
# textblob
# spellchecker

# Spelling correctors including dutch:
# Jamspell

pspell = phunspell.Phunspell('nl_NL')

def phunspell(sentence):
    words = sentence.split()
    counter = 0
    for word in words:
        for suggestion in pspell.suggest(word):
            counter += 1
            if counter > 3:
                counter = 0
                break
            print(pspell.lookup(word), word, suggestion)

for sentence in sentences:
    phunspell(sentence)


# → available checkers: ['BertsclstmChecker', 'CnnlstmChecker', 'NestedlstmChecker', 'SclstmChecker', 'SclstmbertChecker', 'BertChecker', 'SclstmelmoChecker', 'ElmosclstmChecker']

extractor = TextExtractor("../data/kranten/Jaren/", 1700, 1709)
statistics = TextStatistics()
statistics.print_wordcount(extractor.txt)

# checker = BertChecker()
# checker.from_pretrained()
# print(checker.correct("Mirna den 14 Novcanber"))
# checker.correct_from_file(src=extractor.save_dir)


