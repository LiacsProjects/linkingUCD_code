import xml.etree.ElementTree as ET


# Retrieve all children using recursion
def childRecursive(tag_element, recursion):
    for tag_child in tag_element:
        if tag_child:
            print("Begin of \"" + tag_child.tag.split("}")[1] + "\":")
            childRecursive(tag_child, True)
        else:
            child_text = "\"" + tag_child.tag.split("}")[1] + "\" " + tag_child.text
            if recursion:
                child_text = "\t" + child_text
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
    for tag in tags:
        for tag_element in root.iter("{http://Mindbus.nl/A2A}" + tag):
            print(tag_element.tag.split("}")[1], tag_element.attrib)
            childRecursive(tag_element, False)
            print("\n")


# main
if __name__ == '__main__':
    count = 1
    base = "record"
    # path = "data/Erfgoed Leiden/final/BS Geboorte_records1.xml"
    path = "data/Erfgoed Leiden/huwelijk.xml"
    with open(path, "r", encoding="utf-8") as f:
        line = f.readline().strip()
        record_tree = ''
        while line:
            if "</record" + str(count) in line:
                print("Record", str(count), "_________________________________________________________________________")
                record_tree += line
                xmlExtractor(ET.ElementTree(ET.fromstring(record_tree)))
                record_tree = ''
                count = count + 1
            else:
                record_tree = line
            line = f.readline().strip()
        f.close()
