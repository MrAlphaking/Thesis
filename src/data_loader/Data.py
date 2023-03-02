from abc import ABC, abstractmethod
import os

import utils.Util
from src.utils.Util import *

class Data(ABC):
    # @abstractmethod
    def __init__(self, save_path):
        self.base_path = f'../../data/Ground Truth/'
        self.save_path = save_path

    @abstractmethod
    def get_data(self):
        pass

    # def get_data_threads(self):
        

    def get_txt(path):
        with open(path, encoding="utf8", errors="ignore") as f:
            lines = f.read().replace("\n", " ").split(".")
            return lines

    def create_year_list(year, count):
        return [year for i in range(count)]

    def merge(list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list

    def read_from_file(self):
        if os.path.exists(self.save_path) and READ_FROM_FILE_INTERMEDIATES:
            return read_pandas(self.save_path)

