from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class DBNL(DataSet):
    """
    This DataSet class is connected to the DataSet found on https://lab.kb.nl/dataset/dbnl-ocr-data-set
    """

    def get_item(self, file, df):
        path = f'{self.base_path}Books 2/TXT'
        Did = file.replace(".txt", "").removesuffix('_01')
        results = self.get_txt(f'{path}/{file}')
        results = ' '.join(results)
        try:
            year = df.loc[df['ti_id'] == Did].reset_index(drop=True).at[0, 'jaar']
            return [(results, year)]
        except:
            print(file)
            print(Did)
            return [(results, '0000')]

    def get_data(self):
        if os.path.exists(self.save_path) and READ_FROM_FILE_INTERMEDIATES:
            return read_pandas(self.save_path)

        print_telegram(f'Reading in Books 2')
        path = f'{self.base_path}Books 2/TXT'
        df = pd.read_excel(f'{BASE_PATH}xlsx/Metadata_DBNL_OCR_v1.xlsx')
        lines = self.multi_thread(os.listdir(path), df, desc='DBNL')

        return_frame = pd.DataFrame(lines, columns=["target", "year"])

        write_pandas(return_frame, self.save_path)
        return return_frame
