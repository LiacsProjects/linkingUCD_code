#
# Adding a new environment variable
#
# Source: https://www.geeksforgeeks.org/python-os-environ-object/
# Python program to explain os.environ object 
#
import os
import sys
import platform

def set_basepath():

    if os.name == "nt":
        # Add a new environment variable
        # Ben van Yperen
        # os.environ['DASHBOARD_BASEPATH'] = 'c:/users/Benva/Jupyter/Dash applications/Linking UCD - dashboard/'

        # Micheal de Koning
        # os.environ['DASHBOARD_BASEPATH'] = 'C:/Users/micha/Documents/Leiden/Univercity/linkingUCD_code/Dashboard/'

        # Richard van Dijk
        os.environ['PLUGINS_BASEPATH'] = 'C:/LiacsProjects/LUCD/linkingUCD_code/Plugins/'

    # Get the value of
    # Added environment variable
    print("Operating System:   ", platform.platform())
    print("Python version:     ", sys.version)
    print("PLUGINS_BASEPATH:   ", os.environ['PLUGINS_BASEPATH'])


set_basepath()
