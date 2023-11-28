# Adding a new environment variable
# Source: https://www.geeksforgeeks.org/python-os-environ-object/
# Python program to explain os.environ object 

# importing os module 
import os

# Add a new environment variable 
# os.environ['DASHBOARD_BASEPATH'] = 'c:/users/Benva/Jupyter/Dash applications/Linking UCD - dashboard/'
os.environ['DASHBOARD_BASEPATH'] = 'C:/Users/micha/Documents/Leiden/Univercity/Database_Connected_Dashboard/dashboard_components/'

# Get the value of
# Added environment variable 
print("DASHBOARD_BASEPATH", os.environ['DASHBOARD_BASEPATH'])
