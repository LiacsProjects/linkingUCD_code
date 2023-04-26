# Adding a new environment variable
# Source: https://www.geeksforgeeks.org/python-os-environ-object/
# Python program to explain os.environ object 
  
# importing os module 
import os
import sys
import platform

if os.name == "nt":
    # Add a new environment variable
    os.environ['DASHBOARD_BASEPATH'] = 'c:/users/Benva/PycharmProjects/linkingUCD_code/Dashboard/'
    #os.environ['DASHBOARD_BASEPATH'] = 'C:/Users/micha/Documents/Leiden/Univercity/linkingUCD_code/Dashboard/'

# Get the value of
# Added environment variable
print("Operating System:", platform.platform())
print("Python version:", sys.version)
print("DASHBOARD_BASEPATH:", os.environ['DASHBOARD_BASEPATH'])