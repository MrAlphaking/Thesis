import unittest
from data_loader.DataLoader import clean_dataframe
import pandas as pd
class DataCleanerTest(unittest.TestCase):
    def get_cleaning_dataset(self):
        data = [[' Lorem ipsum dolor sit amet, 5 consectetur adipiscing elit\n', 2020],
                ['sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 2020],
                ['Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 2020]]
        df = pd.DataFrame(data, columns=['target', 'year'])
        return df

    def test_trailing_zeros(self):
        df = self.get_cleaning_dataset()
        df = clean_dataframe(df)
        self.assertTrue(df['target'].iloc[0][0] != ' ')

    def test_remove_enters(self):
        df = self.get_cleaning_dataset()
        df = clean_dataframe(df)
        self.assertTrue("\n" not in df['target'].iloc[0])

    def test_remove_numbers(self):
        df = self.get_cleaning_dataset()
        df = clean_dataframe(df)
        self.assertTrue(not any(char.isdigit() for char in str(df['target'].iloc[0])))