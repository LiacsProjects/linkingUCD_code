import sys, os
sys.path.insert(0, '/home/csunivercity/dashboard')
os.environ['DASHBOARD_BASEPATH'] = "/home/csunivercity/dashboard/"

# need 'server', not 'app', see
# https://community.plotly.com/t/dash-pythonanywhere-deployment-issue/5062/2
from dashboard import server as application
