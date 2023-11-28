# # ****************************************************************************************** LOCAL
# # added for local server
# # extra regel om environmental variable te bepalen
# # ******************************************************************************************  end local
# # import modules
# import dash_bootstrap_components as dbc
# import dash_daq as daq
# import pandas as pd
# from dash import Dash, dcc, html, Input, Output, ctx, ALL, callback
# # import figures_components
# import random
# import visdcc
# import dash
# import networkx as nx
# import plotly.graph_objs as go
# import matplotlib.pyplot as plt
#
# dash.register_page(__name__)
#
# layout = dbc.Container(children=[
#     dbc.Row([
#         dbc.Col([
#             # html.Div(children=[
#             #     visdcc.Network(id='net', data=dict(), options=dict(height='600px', width='80%'))
#             # ], id='network-div'),
#             html.Div(children=[], id='network-div'),
#             dbc.Button('Generate Network', id='network-button')
#         ])
#     ])],
#     fluid=True)
#
# rl_df = pd.read_csv(
#     'H:/Documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard_research_tool/pages/RL Gelinkte Personen.csv',
#     sep=';')
# relations_df = pd.read_csv(
#     'H:/Documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard_research_tool/pages/relations_all.csv')
#
#
# # relations van 1 individu vinden
# def relations_to_person(unique_person_id):
#     """
#     Looks up one person in the rl_df, this person has many certificates to their name,
#     these certificates are looked up in the relations_df, finding links between people
#     the links are registered, and the id's (from the rl_df) are stored
#     """
#     person_data = rl_df[rl_df['unique_person_id'] == unique_person_id]
#     names = list(person_data['name'].unique())
#
#     relations = []
#     relations_id = []
#     counter = 0
#
#     # edges is a list in this form [(unique_person_id_1, unique_person_id_2), relation_type, name_1, name_2, year]
#     # the unique_person_id comes from the Rl Gelinkte Personen file
#     edges = []
#
#     for certificate in person_data['uuid']:
#         # found an edge from the unique_person_id in this function to someone else
#         if len(relations_df[relations_df['uuid_1'] == certificate]):
#             # the relation in the relations_df
#             relation = relations_df[relations_df['uuid_1'] == certificate]
#             for single_relation in relation.iterrows():
#                 relations.append(single_relation[1])
#
#                 # the id from rl_df from the 'other' person in the relation
#                 uuid_2 = single_relation[1].loc['uuid_2']
#                 try:
#                     unique_person_id_2 = int(rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
#                 except TypeError:
#                     # print('typeerror', rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
#                     unique_person_id_2 = None
#
#                 relations_id.append(unique_person_id_2)
#
#                 # print(single_relation)
#                 # print(unique_person_id)
#                 # print(unique_person_id_2)
#
#                 certificate_person_data = person_data.iloc[counter]
#
#                 edges.append([(unique_person_id, unique_person_id_2), relation['relation_type'].iloc[0]])
#             # print('\n\n')
#
#         # found an edge from someone else to the unique_person_id in this function
#         if len(relations_df[relations_df['uuid_2'] == certificate]):
#             # the relation in the relations_df
#             relation = relations_df[relations_df['uuid_2'] == certificate]
#             for single_relation in relation.iterrows():
#                 relations.append(single_relation[1])
#
#                 # the id from rl_df from the 'other' person in the relation
#                 uuid_2 = single_relation[1].loc['uuid_1']
#                 try:
#                     unique_person_id_2 = int(rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
#                 except TypeError:
#                     # print('typeerror', rl_df[rl_df['uuid'] == uuid_2]['unique_person_id'])
#                     unique_person_id_2 = None
#
#                 relations_id.append(unique_person_id_2)
#
#                 # print(single_relation)
#                 # print(unique_person_id)
#                 # print(unique_person_id_2)
#
#                 certificate_person_data = person_data.iloc[counter]
#
#                 edges.append([(unique_person_id_2, unique_person_id), relation['relation_type'].iloc[0]])
#             # print('\n\n')
#         counter += 1
#
#     # edge[0][0] == child, edge[0][1] == parent
#     return edges, relations_id
#
#
# def find_edges(unique_person_id, depth, completed_ids):
#     print(depth)
#     if unique_person_id not in completed_ids:
#         edges, next_id_list = relations_to_person(unique_person_id)
#         completed_ids.append(unique_person_id)
#         depth -= 1
#         if depth:
#             for next_id in next_id_list:
#                 new_edges = find_edges(next_id, depth, completed_ids)
#                 if new_edges:
#                     for new_edge in new_edges:
#                         edges.append(new_edge)
#         return edges
#
#
# @callback(
#     Output('network-div', 'children'),
#     Input('network-button', 'n_clicks')
# )
# def network(network_button):
#     if ctx.triggered_id == 'network-button':
#         depth = 7
#         edges_relations = find_edges(1, depth, [])
#
#         processed_edges = []
#
#         # first create the graph with networkx
#         G = nx.Graph()
#         for edge_relations in edges_relations:
#             print(edge_relations)
#             if edge_relations not in processed_edges and edge_relations[0][0] and edge_relations[0][1]:
#                 G.add_edge(*(edge_relations[0][0], edge_relations[0][1]))
#                 processed_edges.append(edge_relations)
#
#         pos = nx.spring_layout(G)
#
#         # Create Edges
#         final_edges_list = []
#
#         edge_x = []
#         edge_y = []
#         mnode_x, mnode_y, mnode_txt = [], [], []
#
#         edge_text_counter = 0
#         for edge in G.edges():
#             x0, y0 = pos[edge[0]]
#             x1, y1 = pos[edge[1]]
#             edge_x.append(x0)
#             edge_x.append(x1)
#             edge_x.append(None)
#             edge_y.append(y0)
#             edge_y.append(y1)
#             edge_y.append(None)
#
#             mnode_x.extend([(x0 + x1) / 2])
#             mnode_y.extend([(y0 + y1) / 2])
#             relation_type = 'No relation type found'
#             for processed_edge in processed_edges:
#                 if processed_edge[0] == edge or (processed_edge[0][1], processed_edge[0][0]) == edge:
#                     print(processed_edge[0], edge, processed_edge[1])
#                     relation_type = processed_edge[1]
#                     break
#             mnode_txt.extend([f"{relation_type}"])
#
#             edge_text_counter += 1
#
#         edge_trace = go.Scatter(
#             x=edge_x, y=edge_y,
#             line=dict(width=0.5, color='#888'),
#             hoverinfo='text',
#             mode='lines',)
#
#         mnode_trace = go.Scatter(x=mnode_x, y=mnode_y, mode="markers", showlegend=False,
#                                  hovertemplate="Edge %{hovertext}<extra></extra>",
#                                  hovertext=mnode_txt, marker=go.Marker(opacity=0))
#
#         node_x = []
#         node_y = []
#         for node in G.nodes():
#             x, y = pos[node]
#             node_x.append(x)
#             node_y.append(y)
#
#         node_trace = go.Scatter(
#             x=node_x, y=node_y,
#             mode='markers',
#             hoverinfo='text',
#             marker=dict(
#                 showscale=True,
#                 # colorscale options
#                 # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
#                 # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
#                 # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
#                 colorscale='YlGnBu',
#                 reversescale=True,
#                 color=[],
#                 size=10,
#                 colorbar=dict(
#                     thickness=15,
#                     title='Node Connections',
#                     xanchor='left',
#                     titleside='right'
#                 ),
#                 line_width=2),
#             )
#
#         node_adjacencies = []
#         node_text = []
#         for node, adjacencies in enumerate(G.adjacency()):
#             node_adjacencies.append(len(adjacencies[1]))
#             node_text.append(f'{list(G.nodes())[node]}\n# of connections: ' + str(len(adjacencies[1])))
#
#         node_trace.marker.color = node_adjacencies
#         node_trace.text = node_text
#
#         fig = go.Figure(data=[edge_trace, node_trace, mnode_trace],
#                         layout=go.Layout(
#                             hovermode='closest',
#                             showlegend=False,
#                             xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                             yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                             width=1200,
#                             height=1000
#                         ),
#
#
#                         )
#
#         return dcc.Graph(figure=fig)
