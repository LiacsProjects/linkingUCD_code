import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date


#convert csv to df
hoogleraren = pd.read_csv("Database/csvs/Hoogleraren.csv", delimiter=';')

#test if ages are valid
hoogleraren["geboortedatum"] = pd.to_datetime(hoogleraren["geboortedatum"], errors='coerce')
hoogleraren = hoogleraren.dropna(subset=["geboortedatum"])
hoogleraren["Sterfdatum"] = pd.to_datetime(hoogleraren["Sterfdatum"], errors='coerce')
hoogleraren = hoogleraren.dropna(subset=["Sterfdatum"])
hoogleraren["age"] = (hoogleraren["Sterfdatum"].dt.year - hoogleraren["geboortedatum"].dt.year)
hoogleraren["age"] = hoogleraren["age"].sort_values(ascending=False)
#max age is 100
print(hoogleraren["age"].max())
print(hoogleraren.shape)
