import DataCleaner
import matplotlib.pyplot as plt
import pandas as pd

df = DataCleaner.get_data()

# ax = df.plot.hist(bins=12, alpha=0.5)
# pd.value_counts(df['year']).plot.bar()
years = list(df['year'])
fig, ax = plt.subplots(figsize =(10, 7))
bins = []
ax.hist(years, bins = [1600,1650,1700,1750,1800,1850,1900,1950,2000,2023])
plt.show()