from urllib.request import urlopen
import xml.etree.ElementTree as ET
import re
import datetime

class Delpher:
    def __init__(self):
        print("Delpher class created")
        self.year_dict = {}

    def get_image(self, identifier):
        url = f'http://resolver.kb.nl/resolve?urn={identifier}:p001:image'

    def get_year(self, identifier):


        if identifier in self.year_dict:
            # print('In dict')
            return self.year_dict[identifier]


        url = f'https://services.kb.nl/mdo/oai/dd69d73d-91c0-43a5-8516-2ccf458a158a?verb=GetRecord&identifier=DDD:{identifier}&metadataPrefix=didl'
        # print(url)
        with urlopen(url) as f:
            tree = ET.parse(f)
            root = tree.getroot()

            dates = root.findall('.//{http://purl.org/dc/elements/1.1/}date')

            if len(dates) > 0:
                date_object = datetime.datetime.strptime(dates[0].text, "%Y-%m-%d").date()
                year = str(date_object.year)
                self.year_dict[identifier] = year
                return year
            else:
                self.year_dict[identifier] = '0000'
                return '0000'