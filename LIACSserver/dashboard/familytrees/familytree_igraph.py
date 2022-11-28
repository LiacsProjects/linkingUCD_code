import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
import data

family = data.testfamily
"""
nr_vertices = len(family)
g = Graph()
g.add_vertices(nr_vertices)
root = family.loc[family['Relation'] == 'Earliest Ancestor', 'Person 1'].iloc[0]
print(root)
print(g.vs)
"""
#"""
nr_vertices = len(family)
print('nr_vertices: ' + str(nr_vertices))
v_label = list(map(str, range(nr_vertices)))
print('v_label:')
print(v_label)
G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
print('G')
print(G)
lay = G.layout('rt')
print('lay')
print(lay)

position = {k: lay[k] for k in range(nr_vertices)}
print('position:')
print(position)
Y = [lay[k][1] for k in range(nr_vertices)]
print('Y:')
print(Y)
M = max(Y)

es = EdgeSeq(G)  # sequence of edges
print('es:')
print(es)
E = [e.tuple for e in G.es]  # list of edges
print('E:')
print(E)

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2 * M - position[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe += [position[edge[0]][0], position[edge[1]][0], None]
    Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

labels = v_label

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=Xe,
    y=Ye,
    mode='lines',
    line=dict(color='rgb(210,210,210)', width=1),
    hoverinfo='none'
))
fig.add_trace(go.Scatter(
    x=Xn,
    y=Yn,
    mode='markers',
    name='bla',
    marker=dict(symbol='circle-dot',
                size=18,
                color='#6175c1',  # '#DB4551',
                line=dict(color='rgb(50,50,50)', width=1)
                ),
    text=labels,
    hoverinfo='text',
    opacity=0.8
))


def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
    L = len(pos)
    if len(text) != L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k],  # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2 * M - position[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations


axis = dict(
    showline=False,  # hide axis line, grid, ticklabels and  title
    zeroline=False,
    showgrid=False,
    showticklabels=False,
)

fig.update_layout(
    annotations=make_annotations(position, v_label),
    font_size=12,
    showlegend=False,
    xaxis=axis,
    yaxis=axis,
    margin=dict(l=0, r=0, b=0, t=0),
    hovermode='closest',
    plot_bgcolor='rgb(223,223,218,0.7)'
)
#"""
fig.show()
