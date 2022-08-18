from urllib.request import urlopen
import database
import json
import pandas as pd

"""
Description of input parameters for Records/Search:

Name            Required	Description
name	        Yes	        Search query (see search examples on front page for advances queries, can include 2 names
                            separated by & and year/period)
archive	        No	        Filter returned search results on archive (obtain a list of valid archive codes via
                            Stats/Archives)
                                - elo = Erfgoed Leiden en Omstreken
number_show     No	        Number of results to show (max=100), default = 10
sourcetype	    No	        Filter results on source type (obtain a list of valid source types via Stats/Source types)
eventplace	    No	        Filter results on event place
relationtype	No	        Filter results on relation type
sort	        No	        Column to sort the results on (negative value to sort descending, positive ascending):
                                - 1 = Name (default)
                                - 2 = Role
                                - 3 = Event
                                - 4 = Date
                                - 5 = Place
                                - 6 = Source
lang	        No	        Language code, "nl" for Dutch (default) and "en" for English - this has only effect on the
                            name of the archive, the sourcetype, the relationtype and the eventtype values in the
                            search results.
callback	    No	        Function name to be called on JSON data
start	        No	        Initial results to return (for paging), default = 0
"""


def constructQuery():
    print("Parameters:")
    print("<name>, <archive>, <number_show>, <sourcetype>, <eventplace>, <relationtype>, "
          "<sort>, <lang>, <callback>, <start>")
    print("Note: <name> is required and fill in '-' if you don't want to specify the parameter")
    print("Enter parameters in CSV format ('-' for empty parameter):")
    query = input()
    return query


def classifyRecordLink(prof_records, persons, event):
    """
    Returns a classification of a link between two records based on several factors
        :param prof_records: professor record(s) from database
        :param persons: person record(s) from external source
        :param event: linkage event
        :return: classification of a link between two records based on several factors
    """
    """
    To compare for Marital records are dates and places. For example:
    Places of birth, death, residence
    Wedding date: check if (internal) person age is compatible with wedding date
    Check if profession is "professor" related
    
    Constraint based, if "checklist" fails, classification is non-, or potential link
    """

    return


# Return a list of identifiers from records that contain a certain name
def getIdentifiers(query):
    query = query.split(", ")
    if len(query) < 10:
        print("Missing parameter(s)!", query)
        return None
    elif len(query) > 10:
        print("Too many parameters!", query)
        return None
    query = [parameter.replace('-', '') for parameter in query]
    query = [parameter.replace(' ', '%20') for parameter in query]
    url = "https://api.openarch.nl/1.0/records/search.json?name=%s&archive=%s&number_show=%s&sourcetype=%s" \
          "&eventplace=%s&relationtype=%s&sort=%s&lang=%s&callback=%s&start=%s" % tuple(query)

    response = urlopen(url)
    data_json = json.loads(response.read())

    # Pretty print json
    # print(json.dumps(data_json, indent=4))

    if data_json["response"]["number_found"] == 0:
        return []

    # Append all identifiers to a list
    identifiers = []
    for record in data_json["response"]["docs"]:
        identifiers.append(record["identifier"])

    # When there are more than 100 records found, more requests are needed
    number_of_records_found = int(data_json["response"]["number_found"])
    requested_records = int(query[2])
    start = int(query[9])
    if (requested_records + start) < number_of_records_found:
        query[9] = str(start + requested_records)
        new_query = ', '.join(map(str, query))  # Convert list to csv string
        identifiers = identifiers + getIdentifiers(new_query)

    return identifiers


# Extract data from single record and return df
def readRecord(identifier, prof_record):
    # url = "https://api.openarch.nl/1.0/records/show.json?archive=elo&identifier=" + identifier
    # response = urlopen(url)
    # data_json = json.loads(response.read())

    # For local processing of JSON file
    f = open("OA_Identifier.json")
    data_json = json.load(f)

    """
    Each Erfgoed Leiden record has four head items:
        1 - a2a_Person
        2 - a2a_Event
        3 - a2a_RelationEP
        4 - a2a_Source
    Note: data_json[0] contains the tags above from a recordPersonNameFirstName
    """

    sourceLink = data_json[0]['a2a_Source']['a2a_SourceDigitalOriginal']['a2a_SourceDigitalOriginal']
    person_dict = {'PersonID': None, 'TypeOfPerson': None, 'a2a_PersonNameFirstName': None, 'a2a_PersonNameLastName': None, 'FamilyName': None,
                   'a2a_PersonNamePrefixLastName': None, 'a2a_PersonNameNickName': None, 'a2a_Gender': None,
                   'a2a_Origin': None, 'a2a_BirthPlace': None, 'a2a_Religion': None, 'a2a_Status': None, 'a2a_Profession': None,
                   'a2a_PersonRemark': None}
    relation_dict = {'a2a_PersonKeyRef': None, 'a2a_RelationType': None}
    event_dict = {'a2a_EventType': None, 'a2a_Date': None, 'a2a_EventPlace': None}

    # Maybe include a2a_Source if deemed necessary
    person_dicts = parseHeadItem(data_json[0]['a2a_Person'], person_dict)
    relation_dicts = parseHeadItem(data_json[0]['a2a_RelationEP'], relation_dict)
    for relation in relation_dicts:  # connect 'pid' to type of relation
        for person in person_dicts:
            if relation['a2a_PersonKeyRef'] == person['pid']:
                person['TypeOfRelation'] = relation['a2a_RelationType']
                continue
    event_dict['a2a_EventType'] = data_json[0]['a2a_Event']['a2a_EventType']['a2a_EventType']
    event_dicts = parseEventItem(data_json[0]['a2a_Event'], event_dict)
    print(event_dicts)
    classifyRecordLink(prof_record, person_dicts, event_dicts)

    # relation_df = pd.DataFrame(data, columns=['RelationID', 'TypeOfRelation', 'FromPersonID', 'ToPersonID', 'Event', 'EventDate', 'EventPlace', 'SourceName', 'SourceWebLink', 'SourceRating', 'LinkClass', 'Remark'])
    # person_df = pd.DataFrame(list(person_dicts), columns=['PersonID', 'TypeOfPerson', 'PersonNameFirstName', 'PersonNameLastName',
    #                                            'PersonNamePrefixLastName', 'PersonNameNickName', 'Gender', 'Origin',
    #                                            'Religion', 'Status', 'Profession'])
    # print(person_df.head(5))

    # return df


# TODO: parse 'date' item
def parseEventItem(head_item_json, head_item_dict):
    for attribute in head_item_json:
        if isinstance(head_item_json[attribute], dict):
            for subAttribute in head_item_json[attribute]:
                text = head_item_json[attribute][subAttribute]
                while isinstance(text, dict):
                    text = text[subAttribute]
                head_item_dict[attribute] = text
        else:
            head_item_dict[attribute] = head_item_json[attribute]
    return head_item_dict


# Parse JSON to dict and Dataframe for 'head item tag'
# TODO: merge with parseEventItem to reduce duplicate code
def parseHeadItem(head_item_json, head_item_dict):
    # tag_list = []
    head_item_dicts = []
    Leiden = ['Leijden', 'Leyden']
    for sub_item in head_item_json:
        head_item_dict = dict.fromkeys(head_item_dict.keys(), None)  # Reset all dict values to None for new person
        for attribute in sub_item:
            if isinstance(sub_item[attribute], dict):
                for subAttr in sub_item[attribute]:
                    attribute_text = sub_item[attribute][subAttr]
                    # In case of multiple sub elements, loop until string value is found
                    while isinstance(attribute_text, dict):
                        attribute_text = attribute_text[subAttr]
                    if attribute == 'a2a_PersonRemark':
                        if subAttr == 'a2a_Value':
                            head_item_dict[attribute] = attribute_text
                        continue
                    if attribute == 'a2a_EventKeyRef':
                        continue
                    if subAttr == 'a2a_Place':
                        head_item_dict[attribute] = attribute_text
                    else:
                        head_item_dict[subAttr] = attribute_text
            else:
                head_item_dict[attribute] = sub_item[attribute]

        # TODO: normalize all values
        try:
            if head_item_dict['a2a_BirthPlace'] in Leiden:
                head_item_dict['a2a_BirthPlace'] = 'Leiden'
        except KeyError:
            pass
        head_item_dicts.append(head_item_dict)
        print(head_item_dict)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    return head_item_dicts


# def parseEvent(event_dict):
def processRecords(identifiers, prof_record):
    if len(identifiers) == 0:
        print("No records found")
        return

    count = 1
    # TODO: store records from the same register and compare them to get as much information as possible in one try
    #   For example, there could be multiple marriage records from the same person which each have different additional
    #   information that should be merged into the same relation.
    for i in identifiers:
        print(count, "_______________________________________________")
        readRecord(i, prof_record)
        count += 1


def linkProfessors():
    conn = database.Connection()
    profIDs = conn.getProfIDs()

    trouwen = "DTB Trouwen"  # Doop-, Trouw- en Begraafregister, 106 matches
    huwelijk = "BS Huwelijk"  # Burgerlijke Stand, 272 matches
    for p in profIDs:
        # TODO alter names for more matches, i.e. select only first- and lastname instead of full (multiple) names
        prof = conn.getProfInfo(p[0])[0]
        if prof[1] is None:
            name = prof[0] + ' ' + prof[2]
        else:
            name = prof[0] + ' ' + prof[1] + ' ' + prof[2]
        # name = name.replace(',', '')
        name = '~' + name
        parameter_string = name + ", elo, 100, " + huwelijk + ", -, -, 1, nl, -, 0"
        try:
            identifier_list = getIdentifiers(parameter_string)
        except UnicodeEncodeError:
            print("Cannot process name:", name)
            continue
        # Duplicate identifiers are possible as the same (last)name can occur multiple times in one record
        # So we remove the duplicates as we only need to look up the record once
        identifier_list = list(dict.fromkeys(identifier_list))
        processRecords(identifier_list, prof)
    del conn


# Main
if __name__ == "__main__":
    # linkProfessors()
    conn = database.Connection()
    profIDs = conn.getProfIDs()
    # prof = conn.getProfInfo(profIDs[36][0])[0]
    # print(conn.getProfInfo(profIDs[0][0]))
    # readRecord("d344d58d-c1cd-5db7-7e88-5dcfb0de9334", conn.getProfInfo(profIDs[0][0]))
    del conn
