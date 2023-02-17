import requests
import xmltodict
import xml.etree.ElementTree as ET
import json
class Delpher:
    def __init__(self):
        self.base_url = "http://services.kb.nl/mdo/oai/dd69d73d-91c0-43a5-8516-2ccf458a158a"
        self.search_url = "http://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=50&operation=searchRetrieve&startRecord=1&recordSchema=ddd&x-collection=DDD_krantnr&x-facets=&query=%28date%20within%20%2201-01-1940%2031-12-1945%22%29 "
        self.srw = "{http://www.loc.gov/zing/srw/}"
    def parse_xml_tojson(self, content):
        return xmltodict.parse(content)

    def parse_xml_totree(self, content):
        root = ET.fromstring(content)
        return root

    def print_dict(self, mydict):
        print(mydict['srw:searchRetrieveResponse']['srw:records'])

    def get_request(self, url):
        print(f"Request: {url}")
        return requests.get(url).content

    def print_records(self, mydict):
        print(f"Amount of records: {len(mydict)}")
        for dict in mydict:
            print(dict)

    def get_all_records(self, root):
        dictlist = []
        for child in root.find(f'{self.srw}records'):
            mydict = {}
            for grandchild in child.find(f'{self.srw}recordData'):
                key = grandchild.tag.split("}")[1]
                value = grandchild.text
                mydict[key] = value
            dictlist.append(mydict)
        return dictlist

    def get_first_record(self, root):
        return self.get_all_records(root)[:1]

    # p0001, stands for page 1

    def get_all_articles(self, dictlist):
        for dict in dictlist:
            content = self.get_request(dict['metadataKey'])
            data = self.parse_xml_tojson(content)
            # json_data = json.dumps(data)
            # with open("data.json", "w") as json_file:
            #     json_file.write(json_data)
            print(data['OAI-PMH']['GetRecord']['record']['metadata']['didl:DIDL']['didl:Item']['didl:Item'].keys())

    # def get_all_articles(self, dictlist):
    #
    #     for dict in dictlist:
    #         print(dict['metadataKey'])
    #
    #         content = self.get_request(dict['metadataKey'])
    #         root = self.parse_xml_totree(content)
    #         for article in root.find("{http://www.openarchives.org/OAI/2.0/}GetRecord").find("{http://www.openarchives.org/OAI/2.0/}record").find("{http://www.openarchives.org/OAI/2.0/}metadata").find("{urn:mpeg:mpeg21:2002:02-DIDL-NS}DIDL").find("{urn:mpeg:mpeg21:2002:02-DIDL-NS}Item"):
    #
    #                 print(chilc.tag)
    #             print(f"New article: {dict['metadataKey']}")
    #
    #             print(article.tag, article.text, article.attrib)
    #             self.get_article(article)
    #
    #             #
    #             # for grandchild in child:
    #             # #
    #             #     print(grandchild.tag, grandchild.text)
    #         # print(content)
    #
    #
    # def get_article(self, article):
    #     print("Get_Article")
    #     identifier = article.get('{http://purl.org/dc/elements/1.1/}identifier')
    #     if ("p" or "pdf" or "data") in identifier[len(identifier)-6:len(identifier) - 1]:
    #         return None
    #     else:
    #         print(identifier)
    #         # print(arti)
    #
    #         # print(article.find("{urn:mpeg:mpeg21:2002:02-DIDL-NS}Component"))
    #         # print(article.attrib)
    #         # for part in article.find('{urn:mpeg:mpeg21:2002:02-DIDL-NS}Component'):
    #         #     print(part.tag, part.attrib)


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

    # Placeholder for now
    def get_ocr(self, url):
        content = self.get_request(url)
        return self.get_text(content)


    def search(self, from_date=None, until_date=None, maximum_records=50, words=None):

        if words is None:
            content = self.get_request(self.search_url)
            root = self.parse_xml_totree(content)

            # self.get_first_record(root)
            return self.get_first_record(root)
            # for child in root.find(f'{self.srw}records')[:1]:
            #     for grandchild in child.find(f'{self.srw}recordData'):

                    # print(grandchild.find('{http://www.kb.nl/ddd}metadataKey'))
            # self.print_dict(mydict)
        # words = ' '.join(words)


if __name__ == '__main__':
    delpher = Delpher()
    records = delpher.search()
    print(records)
    delpher.get_all_articles(records)




