from src.data_loader.Data import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class Books2(Data):
    """
    This class allows for the
    """
    def get_data(self):
        # Data.read_from_file()
        print_telegram(f'Reading in Books 2')
        path = f'{self.base_path}Books 2/TXT'
        # print(os.listdir('../../'))
        df = pd.read_excel(f'{BASE_PATH}xlsx/Metadata_DBNL_OCR_v1.xlsx')
        lines = []
        for file in tqdm(os.listdir(path), desc='dbnl_books', token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID):
            Did = file.replace(".txt", "").removesuffix('_01')
            year = df.loc[df['ti_id'] == Did].reset_index(drop=True).at[0, 'jaar']
            results = Data.get_txt(f'{path}/{file}')
            results = [item for sublist in results for item in sublist]
            results = Data.merge(results, Data.create_year_list(year, len(results)))
            lines = [*lines, *results]

        return_frame = pd.DataFrame(lines, columns=["target", "year"])

        write_pandas(df, self.save_path)
        return return_frame