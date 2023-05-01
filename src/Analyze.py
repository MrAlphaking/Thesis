from collections import Counter
from data_loader.DataLoader import *
df = get_data()

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

def print_total_count_by_period(df):
    """
    prints the total amount of sentences per time period
    :param df: The df that contains the sentences
    """
    xtick_dict = get_xticklabels()
    years = list(df['year'])
    years.sort()
    # print(count[years[0]])
    freq = Counter()
    for x in years:
        freq[(x - 1) // 10] += 1
    print(freq.values())
    print(freq.keys())

    for index, key in enumerate(freq.keys()):
        print(f'({xtick_dict[f"{key}0-{key}9"]}, {freq[key]}) %{key}0-{key}9')

def print_vocabulary_per_year(df):
    """
    prints the amount of words in the total vocabulary per year
    :param df: The df that contains the sentences
    """
    years = list(set(df['year']))
    years.sort()
    print(df)
    max = 0
    for year in years:
        df_temp = df[df['year'] == int(year)]
        df_temp.reset_index(drop=True)
        target_texts = list(df_temp['target'])

        target_texts = " ".join(target_texts).lower().strip().split(" ")
        # print(f'before: {len(target_texts)}')
        target_texts = set(target_texts)
        # print(f'After: {len(target_texts)}')

        amount_of_words = len(set(target_texts))
        if amount_of_words > max:
            max = amount_of_words
        print(f'({year}, {amount_of_words})')

    print(f'max value = {max}')


print_vocabulary_per_year(df)
# print_total_count_by_period(df)