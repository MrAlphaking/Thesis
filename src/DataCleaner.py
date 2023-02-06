import os
import xml.etree.ElementTree as ET

MIN_CHARACTERS = 10
MAX_CHARACTERS = 50
def remove_duplicates(sentences):
    seen = set()
    result = []
    for item in sentences:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def clean_statenvertaling(line):
    if len(line) < MIN_CHARACTERS or len(line) > MAX_CHARACTERS:
        return False, line
    elif any(char.isdigit() for char in line):
        return False, line
    line = line.replace("\n", "")
    line = line.replace("<FI>", "")
    line = line.strip()
    return True, line

def get_statenvertaling():
    with open('../../data/Ground Truth/Statenvertaling - 1637') as f:
        lines = f.readlines()
        templines = []

        for line in lines:
            add, line = clean_statenvertaling(line)
            if add:
                templines.append(line)
            # else:
            #     print(line)
        # print(f"{len(templines)} of lines")
        return templines

def get_xml_element(filename, element="Unicode"):
    lines = []
    root = ET.parse(filename).getroot()
    for element in root.attrib:
        if "Location" in element:
            location = root.attrib[element].split(" ")[0]
            break

    location = "{" + location + "}"
    for children in root.findall(f".//{location}Unicode"):
        lines.append(children.text.replace("\n", " "))
    return lines

def get_newspaper():
    path = '../../data/Ground Truth/Newspapers/xml/'
    lines = []
    for file in os.listdir(path):
        filename = path + file
        lines.append(get_xml_element(filename, element="Unicode"))
        # print(lines)
    return lines


def get_data():
    print(len(get_newspaper()))
    return remove_duplicates(get_statenvertaling())
