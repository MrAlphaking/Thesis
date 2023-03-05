from abc import ABC, abstractmethod
import os
from tqdm.contrib.telegram import tqdm
import utils.Util
from src.utils.Util import *
import threading

class DataSet(ABC):
    # @abstractmethod
    def __init__(self, save_path):
        self.base_path = f'../../data/Ground Truth/'
        self.save_path = save_path
    @abstractmethod
    def add_item(self, index, file, df, lines):
        pass

    @abstractmethod
    def get_data(self):
        pass

    def thread_function(self, index, item, df):
        self.add_item()
    def multi_thread(self, item_list, df, desc=""):
        return_list = []
        threads = list()
        for index, item in enumerate(progress_bar(item_list, desc=desc)):
            while psutil.cpu_percent():
                time.sleep(0.01)
            x = threading.Thread(target=self.add_item, args=(index, item, df, return_list, ))
            x.start()
            threads.append(x)

        for thread in progress_bar(threads, desc=f"Joining threads {desc}:"):
            thread.join()
        return return_list


    def get_txt(self,path):
        with open(path, encoding="utf8", errors="ignore") as f:
            lines = f.read().replace("\n", " ").split(".")
            return lines

    def create_year_list(self,year, count):
        return [year for i in range(count)]

    def merge(self,list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list

    def read_from_file(self):
        if os.path.exists(self.save_path) and READ_FROM_FILE_INTERMEDIATES:
            return read_pandas(self.save_path)

