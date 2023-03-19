from src.data_loader.DataSet import *
import os
from tqdm.contrib.telegram import tqdm
from src.utils.Util import *

class Impact(DataSet):
    def __init__(self, save_path, type):
        super().__init__(f'{save_path}{type.replace(" ", "_")}' )
        self.type = type
        self.path = f'../../data/Ground Truth/{type}/xml/'

    def get_item(self, file, df):
        Did = int(file.replace(".xml", "").lstrip('0'))
        year = df.loc[df['Did'] == Did].reset_index(drop=True).at[0, 'Dyear']
        filename = self.path + file
        results = get_xml_element(filename, element="Unicode")
        # Flatten list
        results = [item for sublist in results for item in sublist]
        return self.merge(results, self.create_year_list(year, len(results)))
        # lines += results

    def get_data(self):
        if os.path.exists(self.save_path) and READ_FROM_FILE_INTERMEDIATES:
            return read_pandas(self.save_path)

        print_telegram(f'Reading in {self.type}')
        df = pd.read_excel(f'{BASE_PATH}xlsx/impact_{self.type.replace(" ", "_").lower()}.xlsx')

        lines = self.multi_thread(os.listdir(self.path), df, desc=f'Impact {self.path}')

        return_frame = pd.DataFrame(lines, columns=["target", "year"])
        write_pandas(return_frame, self.save_path)
        return return_frame

