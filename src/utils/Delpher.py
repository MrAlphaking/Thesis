import datetime
import os
import urllib
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import cv2

from src.utils.Settings import *
from src.utils.Util import progress_bar


class Delpher:
    """
    A class for querying and downloading images from the Delpher digital library.

    :param save_location: A string representing the folder path where the images will be saved.
    """
    def __init__(self):
        print("Delpher class created")
        self.year_dict = {}
        self.save_location=SAVE_PATH_DOWNLOAD_IMAGE

    def query(self, start_year, end_year, maximum_records):
        """
        Query the Delpher digital library for articles published within a given year.

        :param year: An integer representing the year to search for articles.
        :param maximum_records: An integer representing the maximum number of articles to retrieve.
        :return: A dictionary containing the article metadata.
        """
        url = f"http://jsru.kb.nl/sru/sru?version=1.2&maximumRecords={maximum_records}&operation=searchRetrieve&startRecord=1&recordSchema=ddd&x-collection=DDD_artikel&x-facets=&query=%28date%20within%20%2201-01-{start_year}%2031-12-{end_year}%22%29&x-fields=zones"
        print(url)
        with urlopen(url) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            records = root.findall('.//{http://www.loc.gov/zing/srw/}record')
            return_set = {}
            for record in records:
                key = record.find('.//{http://www.kb.nl/ddd}metadataKey').text
                if key not in return_set:
                    record_item = \
                        {'ocr': record.find('.//{http://purl.org/dc/elements/1.1/}identifier').text,
                         'zones': record.find('.//zones').text,
                         'page_url': record.find(".//{http://www.kb.nl/ddd}pageurl").text,
                         'image': f'http://resolver.kb.nl/resolve?urn={record.find(".//{http://www.kb.nl/ddd}pageurl").text}:image'}
                    return_set[key] = record_item
        return return_set

    def download_images_period(self, start_year, end_year, maximum_records=10, step_size=1):
        for year in progress_bar(range(start_year, end_year, step_size)):
            self.download_images(year, year + step_size, maximum_records=maximum_records)

    def download_images(self, start_year, end_year, maximum_records):
        result_dict = self.query(start_year, end_year, maximum_records)
        path = f'{self.save_location}/{start_year}-{end_year}/'
        if not os.path.exists(path):
            os.makedirs(path)
        # print(result_dict)
        for key in result_dict:
            item = result_dict[key]

            try:
                urllib.request.urlretrieve(item['image'], f'{path}{item["page_url"].replace(":","-")}.jp2')
            except:
                print(f"Error given for {item['image']}")


    def get_year(self, identifier):
        if identifier in self.year_dict:
            # print('In dict')
            return self.year_dict[identifier]
        # "https://services.kb.nl/mdo/oai/dd69d73d-91c0-43a5-8516-2ccf458a158a?verb=GetRecord&identifier=KRANTEN:MMKB23:MMKB23:001577139:mpeg21&metadataPrefix=didl"
        url = f'https://services.kb.nl/mdo/oai/{delpher_api_key}?verb=GetRecord&identifier=DDD:{identifier}&metadataPrefix=didl'
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