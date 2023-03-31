
from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class DataSetDelpher(DataSet):
    def __init__(self, save_path, delpher):
        super().__init__(save_path)
        self.delpher = delpher

    def get_item(self, file, df):
        pass