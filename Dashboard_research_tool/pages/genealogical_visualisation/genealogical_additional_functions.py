import pandas as pd
from Adapters import database
from textdistance import levenshtein
import networkx as nx
import matplotlib.pyplot as plt


def matches_to_csv():
    # function to find all edges for the networks, too slow to save all of this in an excel file

    conn = database.Connection()
    df = conn.select('person', ['locationStartDate', 'LastName', 'FirstName'], 'LEFT JOIN location ON locationID = personPersonID WHERE TypeOfLocation = 1 ')
    rl_df = pd.read_csv('RL Gelinkte Personen.csv', sep=';')
    print(min(rl_df['year']))

    rl_series_unique = rl_df['name'].unique()

    final_df = pd.DataFrame()
    database_first_name_column = []
    database_last_name_column = []
    rl_name_column = []
    levenshtein_distance_column = []
    birth_date_column = []

    print(df)
    counter = 0
    for row in df.iterrows():
        print(counter)
        counter += 1

        startdate = row[0]
        try:
            if int(startdate[:4]) < 1700:
                continue
        except TypeError:
            print('error')
        name_series = row[1]
        lastname = name_series[0]
        firstname = name_series[1]
        full_name = firstname.lower().replace(" ", '') + lastname.lower().replace(" ", '')
        print(full_name)
        best_levenshtein = 1000
        for rl_name in rl_series_unique:
            distance = levenshtein.distance(rl_name, full_name)


            # print(rl_name, full_name, distance)

            if distance < best_levenshtein:
                best_levenshtein = distance
                best_match = rl_name

        print(best_match)
        database_first_name_column.append(firstname)
        database_last_name_column.append(lastname)
        birth_date_column.append(startdate)
        rl_name_column.append(best_match)
        levenshtein_distance_column.append(best_levenshtein)



    final_df['database_first_name'] = database_first_name_column
    final_df['database_last_name'] = database_last_name_column
    final_df['database_birth_date'] = birth_date_column
    final_df['rl_name'] = rl_name_column
    final_df['levenshtein_distance'] = levenshtein_distance_column

    final_df.to_csv('results_df.csv', index=False)


def visualise_one_person(rl_name):
    df = pd.read_csv('results_df.csv')
    df_relations = pd.read_csv('relations.csv', sep=';')
    df_rl = pd.read_csv('RL Gelinkte Personen.csv', sep=';')
    df_under_3 = df[df["levenshtein_distance"] <= 2][['database_first_name', 'database_last_name', 'rl_name']]
    uuid = df_rl[df_rl['name'] == rl_name]['uuid']
    print(uuid)
    connections = []
    for id in uuid:
        print(df_relations[df_relations['rel1_id'] == id])
        for row in df_relations[df_relations['rel1_id'] == id]:
            # print(row)
            connections.append(row)
        for row in df_relations[df_relations['rel2_id'] == id]:
            connections.append(row)
    print(connections)


def create_relations():
    """"
    Function to get many of the relations from the certificate excel files
    TODO: likely does not get all of the information from the certificate excel files
    """
    df_echtscheiding = pd.read_csv("Echtscheiding.csv", sep=';')
    df_geboorte = pd.read_csv("Geboorte.csv", sep=';')
    df_overlijden = pd.read_csv("Overlijden.csv", sep=';')
    df_huwelijk = pd.read_csv("Huwelijk.csv", sep=';')

    relations_huwelijk = pd.DataFrame([])

    huwelijk_id1 = []
    huwelijk_id2 = []
    relation_type_huwelijk = []
    akte_id_huwelijk = []
    for index in range(len(df_huwelijk)):
        huwelijk_id1.append(df_huwelijk.loc[index]['Bruidegom-uuid'])
        huwelijk_id2.append(df_huwelijk.loc[index]['Bruid-uuid'])
        relation_type_huwelijk.append('huwelijk')
        akte_id_huwelijk.append(df_huwelijk.loc[index]['uuid'])
        print(index)

    relations_huwelijk['uuid_1'] = huwelijk_id1
    relations_huwelijk['uuid_2'] = huwelijk_id2
    relations_huwelijk['relation_type'] = relation_type_huwelijk
    relations_huwelijk['uuid_akte'] = akte_id_huwelijk

    print(relations_huwelijk)


    # 1 voor vader en 1 voor moeder in de dataframe?
    relations_geboorte = pd.DataFrame([])

    geboorte_id1 = []
    geboorte_id2 = []
    relation_type_geboorte = []
    akte_id_geboorte = []
    for index in range(len(df_geboorte)):
        for parent in ['vader', 'moeder']:
            if parent == 'vader':
                try:
                    geboorte_id1.append(df_geboorte.loc[index]['Kind-uuid'])
                    geboorte_id2.append(df_geboorte.loc[index]['Vader-uuid'])
                    akte_id_geboorte.append(df_geboorte.loc[index]['uuid'])
                    relation_type_geboorte.append('vader')
                except KeyError:
                    geboorte_id1.append(df_geboorte.loc[index]['Kind-uuid'])
                    geboorte_id2.append('missing')
                    akte_id_geboorte.append(df_geboorte.loc[index]['uuid'])
                    relation_type_geboorte.append('vader')
            if parent == 'moeder':
                try:
                    geboorte_id1.append(df_geboorte.loc[index]['Kind-uuid'])
                    geboorte_id2.append(df_geboorte.loc[index]['Moeder-uuid'])
                    akte_id_geboorte.append(df_geboorte.loc[index]['uuid'])
                    relation_type_geboorte.append('moeder')
                except KeyError:
                    geboorte_id1.append(df_geboorte.loc[index]['Kind-uuid'])
                    geboorte_id2.append('missing')
                    akte_id_geboorte.append(df_geboorte.loc[index]['uuid'])
                    relation_type_geboorte.append('moeder')
        print(index)


    relations_geboorte['uuid_1'] = geboorte_id1
    relations_geboorte['uuid_2'] = geboorte_id2
    relations_geboorte['relation_type'] = relation_type_geboorte
    relations_geboorte['uuid_akte'] = akte_id_geboorte

    print(relations_geboorte)


    relations = relations_huwelijk.append(relations_geboorte)


    relations_overlijden = pd.DataFrame([])
    overledene_uuid1 = []
    overledene_uuid2 = []
    akte_uuid_overlijden = []
    relation_type_overlijden = []

    for index in range(len(df_overlijden)):
        overledene_uuid1.append(df_overlijden.loc[index]['Overledene-uuid'])
        akte_uuid_overlijden.append(df_overlijden.loc[index]['uuid'])
        relation_type_overlijden.append('Overleden')

    overledene_uuid2 = overledene_uuid1
    relations_overlijden['uuid_1'] = overledene_uuid1
    relations_overlijden['uuid_2'] = overledene_uuid2
    relations_overlijden['relation_type'] = relation_type_overlijden
    relations_overlijden['uuid_akte'] = akte_uuid_overlijden

    relations = relations.append(relations_overlijden)


    relations_scheiding = pd.DataFrame([])
    scheiding_uuid1 = []
    scheiding_uuid2 = []
    akte_uuid_scheiding = []
    relation_type_scheiding = []

    for index in range(len(df_echtscheiding)):
        scheiding_uuid1.append(df_echtscheiding.loc[index]['Gewezen echtgenoot-uuid'])
        scheiding_uuid2.append(df_echtscheiding.loc[index]['Gewezen echtgenote-uuid'])
        akte_uuid_scheiding.append(df_echtscheiding.loc[index]['uuid'])
        relation_type_scheiding.append('Echtscheiding')

    relations_scheiding['uuid_1'] = scheiding_uuid1
    relations_scheiding['uuid_2'] = scheiding_uuid2
    relations_scheiding['relation_type'] = relation_type_scheiding
    relations_scheiding['uuid_akte'] = akte_uuid_scheiding

    relations = relations.append(relations_scheiding)


    relations.to_csv('relations_all.csv', index=False)


