# Creating dataframe
# Import modules
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
import os
#from pathlib import Path
import data

#base_path = Path(os.environ['DASHBOARD_BASEPATH'])
#base_path_name = os.environ['DASHBOARD_BASEPATH']
image_file = "/assets/professors_780x400.jpeg"

card_professor = dbc.Card([
    dbc.CardImg(
        src="/assets/professors_780x400.jpeg",
        top=True,
        style={"opacity": 0.5},
        class_name="cardImg"
    ),
    dbc.CardImgOverlay(
        dbc.CardBody([
            html.H3("Professors", className="card-title"),
            html.B("Visualizations of professors", className="card-text"),
            dbc.Button("Go to visualizations", id="btn-professor", color="primary", class_name="card-btn", n_clicks=0),
        ]),
    )],
    # style={"width": "22rem"},
    style={"width": "80%", "height": "75%"},
)


card_student = dbc.Card([
    dbc.CardImg(
        src="/assets/Student_400x267.jpg",
        top=True,
        style={"opacity": 0.5},
        class_name="cardImg"
    ),
    dbc.CardImgOverlay(
        dbc.CardBody([
            html.H3("Students", className="card-title"),
            html.B("Visualizations of students", className="card-text"),
            dbc.Button("Go to visualizations", id="btn-student", color="primary", class_name="card-btn", n_clicks=0),
        ]),
    )],
    # style={"width": "22rem"},
    style={"width": "80%", "height": "75%"},
)


card_rectores = dbc.Card([
    dbc.CardImg(
        src="/assets/alumni.jpeg",
        top=True,
        style={"opacity": 0.5},
        class_name="cardImg"
    ),
    dbc.CardImgOverlay(
        dbc.CardBody([
            html.H4("Rectores Magnifici", className="card-title"),
            html.B("Visualizations of Rectores Magnifici", className="card-text"),
            dbc.Button("Go to visualizations", id="btn-rectores", color="primary", class_name="card-btn", n_clicks=0),
        ]),
    )],
    # style={"width": "22rem"},
    style={"width": "80%", "height": "75%", "box-shadow": "0 0 5px 1px rgb(120 110 100 / 30%)"},
)


card_colofon = dbc.Card([
    dbc.CardImg(
        src="/assets/LEI001013879.jpg",
        top=True,
        style={"opacity": 0.5},
        class_name="cardImg",
    ),
    dbc.CardImgOverlay(
        dbc.CardBody([
            html.H3("Colofon", className="card-title"),
            html.B("Sources, contact information and more", className="card-text"),
            dbc.Button("Go to colofon", id="btn-colofon", color="primary", class_name="card-btn", n_clicks=0),
            # dbc.Button("Go to visualizations", color="primary", class_name="butcol"),
        ]),
    )],
    style={"width": "80%", "height": "75%"},
)


home_grid = dbc.Container([
    dbc.Row([
        dbc.Col([card_professor], width={"size": 5, "offset": 1}, style={"margin-bottom": "3%"}),
        dbc.Col([card_student], width={"size": 5, "offset": 1}, style={"margin-bottom": "3%"}),
    ], align="center", justify="center",),
    dbc.Row([
        dbc.Col([card_rectores], width={"size": 5, "offset": 1}),
        dbc.Col([card_colofon], width={"size": 5, "offset": 1}),
    ], align="center", justify="center",),
], fluid=True)

home_content = dbc.Container(id='h_content', className='parent_content',
                             children=[
                                       html.Div(id='h_info', className='container',
                                                children=[
                                                           html.H2('Introduction'),
        html.P('Leiden University was founded in 1575. '
               'Since then, many thousands of students and staff have attended the university. '
               'Who were they? Where did they come from?  '
               'How did the academic population change over time? '
               'This website allows you to explore and visualise the answers to these questions. '
               'You can search for information on students and on academic staff.'),
        html.P('NB. This project is a work-in-progress. The data and functionalities of this website will be regularly updated and improved.'),
        # html.Div(className='center_object', children=[
        #     html.Embed(src='/assets/LEI001013879.jpg', width='40%', height='40%',
        #                title=('Academiegebouw, Rapenburg 73. '
        #                       'Academie met op de voorgrond ijsvermaak op het Rapenburg.'
        #                       'Foto van een tekening in het album Amicorum van Johannes van Amstel '
        #                       'van Mijnden, 1601, in Koninklijke Bibliotheek te Den Haag.')),
        #     html.P('Erfgoed Leiden en Omstreken', style={'font-size': 'small'})
        # ]),
                                                           html.Div(home_grid)
                                                         ]),
                                        ], fluid=True)

profs_content = html.Div(id='p_content', className='parent_content', children=[
    dcc.Tabs(id='p_tab_bar', value='p_tab-1', className='header_tab_bar', children=[
        dcc.Tab(label='Timeline', value='p_tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Subject information', value='p_tab-2', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Geographical information', value='p_tab-3', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Individual information', value='p_tab-4', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Pivot Table', value='p_tab-5', className='child_tab',
                selected_className='child_tab_selected')
    ]),
#    html.H2('Information'),
    html.P('This page shows the information about professors previously working at the university of Leiden.'
           ' Choose one of the following options to see more information.', style={"margin-left": "1%"}),
    html.Div(id='professor_page_content'),
])

students_content = html.Div(id='s_content', className='parent_content', children=[
    dcc.Tabs(id='s_tab_bar', value='s_tab-1', className='header_tab_bar', children=[
        dcc.Tab(label='Timeline', value='s_tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Subject information', value='s_tab-2', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Geographical information', value='s_tab-3', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Individual information', value='s_tab-4', className='child_tab',
                selected_className='child_tab_selected'),
    ]),
#    html.H2('Information'),
    html.P('This page shows the information about student enrollments from the period 1575 to 1812. Choose one of '
            'the following options to see details about the enrollments of students at the university of Leiden.', style={"margin-left": "1%"}),
    html.Div(id='student_page_content'),
])

rector_content = html.Div(id='r_content', className='parent_content', children=[
    dcc.Tabs(id='r_tab_bar', value='r_tab-1', className='header_tab_bar', children=[
        dcc.Tab(label='Timeline', value='r_tab-1', className='child_tab', selected_className='child_tab_selected'),
        dcc.Tab(label='Subject information', value='r_tab-2', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Geographical information', value='r_tab-3', className='child_tab',
                selected_className='child_tab_selected'),
        dcc.Tab(label='Individual information', value='r_tab-4', className='child_tab',
                selected_className='child_tab_selected'),
    ]),
#    html.H2('Information'),
    html.P('This page shows the information about all the rectores magnifici the university of Leiden has had.'
           ' Choose one of the following options to see more information.', style={"margin-left": "1%"}),
    html.Div(id='rector_page_content'),
])

sources_content = html.Div(id='src_content', className='parent_content', children=[
    html.Div(id='src_info', className='container', children=[
        html.H2('About this site'),
        html.P('This website is part of the project Linking City, University and Diversity'
               'This website is work in progress. The dataset is not yet complete, '
               'information on the website will be updated periodically.'),
        html.H2('The project'),
        html.P('This website is part of, and presents the first results of the project '
               'Linking University and City in Leiden 1575-2020. '
               'The aim of the project is to examine the interaction between the university and the city. '
               'The impact of the presence of the university on the city has been described '
               'from different perspectives, but we know little about the interaction between '
               'the changing populations in town and gown. '
               'The presence of an academic population affected the urban demography, '
               'social-economic structures and culture. '
               'The urban dynamics related to migration and socio-economic development '
               'may -vice versa- have had impact on the university. The question is how.'  
               'This project will examine the interaction between university and city through data science methods.'),
        html.H2('Projectteam', style={"text-align":"left"}),
        html.P('Wessel Kraaij (Data Science), Ariadne Schmidt (History), '
               'Joost Visser (Data Science), Richard van Dijk (Data Science), '
               'Michael de Koning (Computer Science), Ben van Yperen (History).'),
        html.H2('Datasources', style={"text-align":"left"}),
        html.P('The following sources are being used for this dashboard:'),
        html.Li('Dataset Martine Zoeteman, Student Population Leiden University 1575-1812 (2011), based upon Album Studiosorum. '
               'For an extensive explanation of the sources see:'  
               'Martine Zoeteman-van Pelt, De studentenpopulatie van de Leidse universiteit, 1575-1812; :'
               ' "Een volk op zyn Siams gekleet eenige mylen van Den Haag woonende" (Leiden 2011).'),
        html.Li(children=[
            html.A("https://hoogleraren.universiteitleiden.nl/ ",
                   href="https://hoogleraren.universiteitleiden.nl/"),
           'More information about this source can be found at ',
            html.A("https://hoogleraren.universiteitleiden.nl/toelichting",
                    href="https://hoogleraren.universiteitleiden.nl/toelichting"),
                          ]),
        html.Li('Additional information on rectors magnifici is retrieved from Wikipedia'),
        html.H2('Student projects', style={"text-align":"left"}),
        html.Li('Liam van Dreumel, ‘Visualisation tools to support historical research on a linked dataset about Leiden University’ BA thesis Computer Science, Leiden University.'),
        html.Li(children=['Rick Schreuder, ‘Design of a database supporting the exploration of historical documents and linked register data’ ',
                          html.A("(BA thesis Computer Science, Leiden University).", href="https://theses.liacs.nl/pdf/2021-2022-SchreuderRRJ.pdf")]),
        html.Li(children=['Michael de Koning ‘Extraction, transformation, linking and loading of cultural heritage data’ ',
                          html.A("(BA thesis Computer Science, Leiden University).", href="https://theses.liacs.nl/pdf/2021-2022-KoningMde.pdf")]),
        html.H2('Credits', style={"text-align":"left"}),
        html.P('We like to thank Martine Zoeteman, Saskia van Bergen, Stelios Paraschiakos, Antonis Somorakis, Wout Lamers, '
               'Leida van Hees and Carel Stolker for their contributions to this project. '),
        html.H2('Contact', style={"text-align":"left"}),
        html.P('Ariadne Schmidt,  Wessel Kraaij'),
    ]),
])