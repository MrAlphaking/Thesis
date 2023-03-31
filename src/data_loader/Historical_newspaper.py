from src.data_loader.DataSet import *
from src.data_loader.DataSetDelpher import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *
import re

class HistoricalNewspaper(DataSetDelpher):

    def get_data(self):
        if os.path.exists(self.save_path) and READ_FROM_FILE_INTERMEDIATES:
            return read_pandas(self.save_path)

        logging.info(f'Reading in historical newspapers')
        df = pd.read_csv(f'{BASE_PATH}Newspapers 2/historical_newspaper_groundtruth.csv')
        years = []
        # print(df.columns)

        for item in tqdm(list(df["identifier"]), desc='historical newspaper', token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID):
            item = re.sub('_[0-9][0-9][0-9].jp2_ocr', '', item).replace("_", ":").lower() + ":mpeg21"
            year = self.delpher.get_year(item)
            years.append(year)

        df['year'] = years
        df = df.drop(['Unnamed: 0', 'identifier', 'ocr text'], axis=1)
        df = df.rename(columns={'gt text': 'target'})

        write_pandas(df, SAVE_PATH_HISTORICALNEWSPAPERS)
        return df