import os
import re

class TextExtractor:
    def __init__(self, root_dir, year_lower, year_upper):
        self.year_lower = year_lower
        self.year_upper = year_upper
        self.root_dir = "../data/kranten/Jaren/"
        self.save_dir = f'../data/kranten/{str(year_lower)}-{str(year_upper)}'
        self.txt = []

        if os.path.isfile(self.save_dir):
            self.load()
        else:
            self.txt = []
        print("Extractor created")

    def start(self):
        for year in range(self.year_lower, self.year_upper + 1):
            print(year)
            return_txt = self.get_text_year(year)
            self.txt.extend(return_txt)

    def get_text(self, text):
        lines = []

        for line in text:
            if "xml" in line or "text>" in line or line == "\n":
                continue
            else:
                line = line.replace("<title>", "").replace("</title>", "").replace("<p>", "").replace("</p>","").replace("\n","")
                if re.search('[a-zA-Z]', line):
                    # print(line)
                    lines.append(line)
        return lines

    def get_text_year(self, year):
        print(year)
        # print(directory + str(year))

        month_path = self.root_dir + str(year)

        for directory in os.walk(month_path):
            print(directory[0])
            for file in directory[2]:
                if "articletext" in file:
                    file = f"{directory[0]}\{file}"
                    # print(file)
                    with open(file, encoding='cp850') as txtfile:
                        txt_lines = txtfile.readlines()
                        # get_text(txtfile)
                        txt.extend(self.get_text(self, txt_lines))

    def load(self):
        print("Loading from file")
        with open(self.save_dir, encoding='cp850') as txtfile:
            self.txt = txtfile.readlines()
            # print(self.txt)

    def save(self):
        with open(self.save_dir, 'w', encoding='cp850') as f:
            f.write('\n'.join(txt))