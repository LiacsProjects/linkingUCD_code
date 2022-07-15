import xml.etree.ElementTree as ET
import os
import time


# Retrieve all children using recursion
def childRecursive(tag_element, recursion):
    global AalstCounter
    for tag_child in tag_element:
        if tag_child:
            print("Begin of \"" + tag_child.tag.split("}")[1] + "\":")
            childRecursive(tag_child, True)
        else:
            child_text = "\"" + tag_child.tag.split("}")[1] + "\" " + tag_child.text
            if recursion:
                child_text = "\t" + child_text
            if tag_child.tag.split("}")[1] == "PersonNameLastName" and tag_child.text.__contains__("Boerhaave"):
                AalstCounter = AalstCounter + 1
            print(child_text)


# Go through all xml elements per <tag>
def xmlExtractor(tree):
    root = tree.getroot()

    print("Record tag: " + root.tag.split("}")[1])
    identifier = root[0][0].text
    date_stamp = root[0][1].text
    print("Identifier:", identifier)
    print("Date stamp:", date_stamp)
    print('\n')

    tags = ["Person", "Event", "RelationEP", "Source"]
    # tags = ["Person"]
    for tag in tags:
        for tag_element in root.iter("{http://Mindbus.nl/A2A}" + tag):
            print(tag_element.tag.split("}")[1], tag_element.attrib)
            childRecursive(tag_element, False)
            print("\n")


# TODO: interface for specific searches
def fileReader(file_path):
    global AalstCounter
    with open(file_path, "r", encoding="utf-8") as f:
        record_tree = ''
        line = f.readline().strip()
        while line:
            line = line.strip()
            if "</record" in line:
                # print("Record", str(count), "_________________________________________________________________________")
                record_tree += line
                if record_tree.__contains__("Name>Boerhaave<"):
                    # janCounter = janCounter + 1
                    xmlExtractor(ET.ElementTree(ET.fromstring(record_tree)))
                # xmlExtractor(ET.ElementTree(ET.fromstring(record_tree)))
                record_tree = ''
                # janCounter = janCounter + 1
            else:
                record_tree += line
            line = f.readline()
        f.close()


# main
if __name__ == '__main__':
    global AalstCounter
    AalstCounter = 0
    temp = 0
    # Iterate through all files and extract data
    relative_path = "data/Erfgoed Leiden/final/"
    dir_loc = os.path.join(os.path.dirname(__file__), relative_path)
    start = time.time()
    for file in os.listdir(dir_loc):
        fileReader(relative_path + file)
        # print(file, )

    print("Records with Aalst:", AalstCounter)
    print(f"Time: {time.time() - start} seconds")
