import DataCreator
import matplotlib.pyplot as plt
import collections

df = DataCreator.get_dataframe()

# ax = df.plot.hist(bins=12, alpha=0.5)
# pd.value_counts(df['year']).plot.bar()
years = list(df['year'])
sources = list(df['source'])
targets = list(df['targets'])

words_counter = collections.Counter([word for sentence in targets for word in sentence.split()])

print('{} Words.'.format(len([word for sentence in targets for word in sentence.split()])))
print('{} unique words.'.format(len(words_counter)))
print('30 Most common words in the dataset:')
print('"' + '" "'.join(list(zip(*words_counter.most_common(30)))[0]) + '"')

fig, ax = plt.subplots(figsize =(10, 7))
bins = []
ax.hist(years, bins = [1600,1650,1700,1750,1800,1850,1900,1950,2000,2023])
plt.show()