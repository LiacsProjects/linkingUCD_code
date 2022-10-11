import sys
sys.path.insert(0, '/home/csunivercity/application')

# need 'server', not 'app', see
# https://community.plotly.com/t/dash-pythonanywhere-deployment-issue/5062/2
from test import server as application
