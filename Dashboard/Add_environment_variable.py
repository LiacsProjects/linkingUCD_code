# Adding a new environment variable
# Source: https://www.geeksforgeeks.org/python-os-environ-object/
# Python program to explain os.environ object 

# importing os module 
import os
import sys
import platform

if os.name == "nt":
    # Add a new environment variable
    # Ben van Yperen
    # os.environ['DASHBOARD_BASEPATH'] = 'c:/users/Benva/Jupyter/Dash applications/Linking UCD - dashboard/'

    # Micheal de Koning
    # os.environ['DASHBOARD_BASEPATH'] = 'C:/Users/micha/Documents/Leiden/Univercity/linkingUCD_code/Dashboard/'

    # Richard van Dijk
    os.environ['DASHBOARD_BASEPATH'] = 'C:/LiacsProjects/LUCD/linkingUCD_code/Dashboard/'

    # Julian de Boer
    os.environ['DASHBOARD_BASEPATH'] = 'C:/Users/boert/Documents/uni/thesis/code_for_github/linkingUCD_code/Dashboard/'

# Get the value of
# Added environment variable
print("Operating System:", platform.platform())
print("Python version:", sys.version)
print("DASHBOARD_BASEPATH:", os.environ['DASHBOARD_BASEPATH'])

