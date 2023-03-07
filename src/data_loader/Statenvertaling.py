from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class Statenvertaling(DataSet):

    def get_data(self):
        lines = self.get_txt('Statenvertaling - 1637')
        years = self.create_year_list(1637, len(lines))
        df = pd.DataFrame(self.merge(lines, years), columns=["target", "year"])
        return df