import sys, os
sys.path.insert(0, '/home/csunivercity/dashboardleiden1848')
os.environ['DASHBOARD_BASEPATH'] = "/home/csunivercity/dashboardleiden1848/"

# need 'server', not 'app', see
# https://community.plotly.com/t/dash-pythonanywhere-deployment-issue/5062/2
from dashboard import server as application
