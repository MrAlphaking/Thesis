import requests

import re
import urllib.request as urllib2
# webUrl = urllib2.urlopen("https://viaveritasvita.info/Bibles/DutchBibles/SV_html/")

dict = {"gn" : 50,
        "ex": 40,
        "lv": 27,
        "nm": 36,
        "dt": 34,
        "jz": 24,
        "ri": 21,
        "ru": 4,
        "1sm": 31,
        "2sm": 24,
        "1kn": 22,
        "2kn": 25,
        "1kr": 29,
        "2kr": 36,
        "ea": 10,
        "ne": 13,
        "es": 10,
        "jb": 42,
        "ps": 150,
        "sp": 31,
        "pr": 12,
        "hl": 8,
        "js": 66,
        "jr": 52,
        "kl": 5,
        "ez": 48,
        "dn": 12,
        "hs": 14,
        "jl": 3,
        "am": 9,
        "ob": 1,
        "jn": 4,
        "mi": 7,
        "na": 3,
        "hk": 3,
        "zf": 3,
        "hg": 2,
        "zc": 14,
        "ml": 4,
        "mt": 28,
        "mk": 16,
        "lk": 24,
        "jh": 21,
        "hd": 28,
        "rm": 16,
        "1ko": 16,
        "2ko": 13,
        "gl": 6,
        "ef": 6,
        "fl": 4,
        "ko": 4,
        "1th": 5,
        "2th": 3,
        "1tm": 6,
        "2tm": 4,
        "tt": 3,
        "fm": 1,
        "hb": 13,
        "jk": 5,
        "1pt": 5,
        "2pt": 3,
        "1jh": 5,
        "2jh": 1,
        "3jh": 1,
        "jd": 1,
        "op": 22
        }

newdict = {
        "op": 22
}

for key, value in dict.items():

    for i in range (1, value + 1):

        webUrl = urllib2.urlopen(f"https://viaveritasvita.info/Bibles/DutchBibles/SV_html/{key}{i}.htm")

        # read the data from the URL and print it
        data = str(webUrl.read())
        data = data.split("<TD VALIGN=top>")
        # data= re.sub("<.*?>","",data[1])
        data = data[len(data) - 1].split("<")[0]

        print(key, i, data)

        # data = data.replace("\n", "")
        # data = data.split("\\n")
        # print(data[3:len(data) - 8])


# data

# x = requests.get('https://viaveritasvita.info/Bibles/DutchBibles/SV_html/gn1.htm')
# print(x.json())