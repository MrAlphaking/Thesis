from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *
from src.data_loader.DataSetDelpher import *
import re

class SeventeenthCentury(DataSetDelpher):

    def get_data(self):
        if os.path.exists(self.save_path) and READ_FROM_FILE_INTERMEDIATES:
            return read_pandas(SAVE_PATH_17THCENTURYNEWSPAPER)
        logging.info(f'Reading in 17th century newspapers')
        df = pd.read_csv(f'{BASE_PATH}17thcenturynewspapers.csv', compression='gzip')
        years = []
        for item in tqdm(list(df["identifier"]), desc='17thcenturynewspaper', token=TELEGRAM_TOKEN,
                         chat_id=TELEGRAM_CHAT_ID):
            item = re.sub(':a[0-9][0-9][0-9][0-9]', '', item)
            year = self.delpher.get_year(item)
            years.append(year)

        df['year'] = years
        df = df.drop(['Unnamed: 0', 'identifier', 'ocr_text'], axis=1)
        df = df.rename(columns={'gt text': 'target'})
        write_pandas(df, SAVE_PATH_17THCENTURYNEWSPAPER)
        return df