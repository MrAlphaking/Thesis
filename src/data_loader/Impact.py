from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class Impact(DataSet):
    def __init__(self, save_path, type):
        super().__init__(save_path)
        self.type = type
        self.path = f'../../data/Ground Truth/{type}/xml/'

    def add_item(self, index, file, df, lines):
        Did = int(file.replace(".xml", "").lstrip('0'))
        year = df.loc[df['Did'] == Did].reset_index(drop=True).at[0, 'Dyear']
        filename = self.path + file
        results = get_xml_element(filename, element="Unicode")
        # Flatten list
        results = [item for sublist in results for item in sublist]
        results = self.merge(results, self.create_year_list(year, len(results)))
        lines += results

    def get_data(self):
        print_telegram(f'Reading in {self.type}')
        df = pd.read_excel(f'{BASE_PATH}xlsx/impact_{self.type.replace(" ", "_").lower()}.xlsx')

        lines = []

        for index, file in enumerate(progress_bar((os.listdir(self.path)[:1]),desc=f'impact {self.path}')):
            self.add_item(index, file, df, lines)

        return_frame = pd.DataFrame(lines, columns=["target", "year"])
        print(return_frame)
        return return_frame
    # def get_data(self):

