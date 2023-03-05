from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class DBNL(DataSet):
    """
    This DataSet class is connected to the DataSet found on https://lab.kb.nl/dataset/dbnl-ocr-data-set
    """

    def add_item(self, file, df, lines):
        path = f'{self.base_path}Books 2/TXT'
        Did = file.replace(".txt", "").removesuffix('_01')
        results = self.get_txt(f'{path}/{file}')
        results = ' '.join(results)
        try:
            year = df.loc[df['ti_id'] == Did].reset_index(drop=True).at[0, 'jaar']
            lines.append((results, year))
        except:
            print(file)
            print(Did)
            lines.append((results, '0000'))

    def get_data(self):
        print_telegram(f'Reading in Books 2')
        path = f'{self.base_path}Books 2/TXT'
        df = pd.read_excel(f'{BASE_PATH}xlsx/Metadata_DBNL_OCR_v1.xlsx')
        lines = []
        self.multi_thread(os.listdir(path), )
        for index, file in enumerate(progress_bar(os.listdir(path), desc='dbnl_books')):
            self.add_item(index, file, df, lines)

        return_frame = pd.DataFrame(lines, columns=["target", "year"])

        print(return_frame.head(3))
        print(return_frame.columns)
        write_pandas(return_frame, self.save_path)
        return return_frame
    # def get_data(self):
    #     print_telegram(f'Reading in Books 2')
    #     path = f'{self.base_path}Books 2/TXT'
    #     df = pd.read_excel(f'{BASE_PATH}xlsx/Metadata_DBNL_OCR_v1.xlsx')
    #     lines = []
    #     for index, file in enumerate(progress_bar(os.listdir(path), desc='dbnl_books')):
    #         self.add_item(index, file, df, lines)
    #
    #     return_frame = pd.DataFrame(lines, columns=["target", "year"])
    #
    #     print(return_frame.head(3))
    #     print(return_frame.columns)
    #     write_pandas(return_frame, self.save_path)
    #     return return_frame