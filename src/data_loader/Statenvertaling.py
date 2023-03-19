from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class Statenvertaling(DataSet):

    def get_item(self, item, df):
        pass
    def get_data(self):
        if os.path.exists(self.save_path) and READ_FROM_FILE_INTERMEDIATES:
            return read_pandas(self.save_path)
        print_telegram(f'Reading in Statenvertaling')
        lines = self.get_txt('../../../data/Ground Truth/Statenvertaling - 1637')
        years = self.create_year_list(1637, len(lines))
        df = pd.DataFrame(self.merge(lines, years), columns=["target", "year"])
        write_pandas(df, self.save_path)
        return df