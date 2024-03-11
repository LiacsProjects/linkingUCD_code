#
# Imports
#
import configparser
import os

from Plugins.Data import exceldata as data

#
# Global constants
#
CENTURY_STEP = 1
YEAR_STEP = 5
MARK_SPACING = 10
START_CENTURY = 16

DEFAULT_SUBJECT  = 'Appointment'
SUBJECT_DROPDOWN = ['Gender', 'Birth', 'Birth place', 'Birth country', 'Death', 'Death place',
                    'Death country', 'Promotion', 'Promotion type', 'Promotion place', 'Appointment',
                    'Job', 'Subject area', 'Faculty', 'End of employment']

DEFAULT_GRAPH_SUBJECT  = 'Appointment'
GRAPH_SUBJECT_DROPDOWN = ['Gender', 'Birth', 'Death', 'Promotion', 'Promotion type', 'Appointment',
                          'Job', 'Subject area', 'Faculty', 'End of employment']

DEFAULT_GRAPH  = 'Bar graph'
GRAPH_DROPDOWN = ['Bar graph', 'Line graph', 'Scatter graph']
GRAPH_CONFIG   = {'modeBarButtonsToRemove': ['toImage'], 'displayModeBar': True, }

THESIS_COLUMN_NAME       = 'Thesis'
SUBJECT_AREA_COLUMN_NAME = 'Subject area'
JOB_COLUMN_NAME          = 'Job'

#
# Global vars
#
current_century = data.all_dates_df[(data.all_dates_df['century'] <= START_CENTURY)]

years = []
for y in current_century['year'][0::YEAR_STEP]:
    years.append(y)
years.append(current_century['year'].max())

#config = configparser.ConfigParser()
#config.read(os.environ['PLUGINS_BASEPATH'] + 'assets/config.ini')
#mapbox_token = config['mapbox']['token']
