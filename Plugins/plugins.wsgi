import sys, os
sys.path.insert(0, '/home/csunivercity/plugins')
os.environ['PLUGINS_BASEPATH'] = "/home/csunivercity/plugins/"

# need 'server', not 'app', see
# https://community.plotly.com/t/dash-pythonanywhere-deployment-issue/5062/2
from plugins import server as application
