# Adding a new environment variable
# Source: https://www.geeksforgeeks.org/python-os-environ-object/
# Python program to explain os.environ object 
  
# importing os module 
import os

# Ben van Yperen
# os.environ['DASHBOARD_BASEPATH'] = 'c:/users/Benva/Jupyter/Dash applications/Linking UCD - dashboard/'

# Micheal de Koning
# os.environ['DASHBOARD_BASEPATH'] = 'C:/Users/micha/Documents/Leiden/Univercity/linkingUCD_code/Dashboard/'

# Richard van Dijk
os.environ['DASHBOARD_BASEPATH'] = 'C:/LiacsProjects/LUCD/linkingUCD_code/Dashboard/'

print("DASHBOARD_BASEPATH = ", os.environ['DASHBOARD_BASEPATH'])
