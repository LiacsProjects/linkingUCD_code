import xml.etree.ElementTree as ET
import os

sub_tags = []


# Retrieve all children using recursion
def childRecursive(tag_element, recursion):
    for tag_child in tag_element:
        if tag_child:
            print("Begin of \"" + tag_child.tag.split("}")[1] + "\":")
            childRecursive(tag_child, True)
        else:
            child_text = "\"" + tag_child.tag.split("}")[1] + "\" " + tag_child.text
            sub_tags.append(tag_child.tag.split("}")[1])
            if tag_child.tag.split("}")[1] == "PersonAgeLiteral":
                print("\"" + tag_child.tag.split("}")[1] + "\" " + tag_child.text)
            if recursion:
                child_text = "\t" + child_text
            print(child_text)


# Go through all xml elements per <tag>
def xmlExtractor(tree):
    root = tree.getroot()

    # print("Record tag: " + root.tag.split("}")[1])
    identifier = root[0][0].text
    date_stamp = root[0][1].text
    print("Identifier:", identifier)
    print("Date stamp:", date_stamp)
    print('\n')

    tags = ["Person", "Event", "RelationEP", "Source"]
    for tag in tags:
        for tag_element in root.iter("{http://Mindbus.nl/A2A}" + tag):
            print(tag_element.tag.split("}")[1], tag_element.attrib)
            childRecursive(tag_element, False)


def fileReader(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        record_tree = ''
        line = f.readline().strip()
        while line:
            line = line.strip()
            if "</record" in line:
                # print("Record", str(count), "______________________________________________________________________")
                record_tree += line
                xmlExtractor(ET.ElementTree(ET.fromstring(record_tree)))
                record_tree = ''
            else:
                record_tree += line
            line = f.readline()
        f.close()


# main
if __name__ == '__main__':
    # Iterate through all files and extract data
    relative_path = "data/Erfgoed Leiden/final/"
    dir_loc = os.path.join(os.path.dirname(__file__), relative_path)
    for file in os.listdir(dir_loc):
        fileReader(relative_path + file)
