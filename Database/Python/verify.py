import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date


#convert csv to df
hoogleraren = pd.read_csv("Database/csvs/Hoogleraren.csv", delimiter=';')

#test if ages are valid
hoogleraren["geboortedatum"] = pd.to_datetime(hoogleraren["geboortedatum"], errors='coerce')
count = hoogleraren["geboortedatum"].isnull().sum()
hoogleraren = hoogleraren.dropna(subset=["geboortedatum"])
hoogleraren["Sterfdatum"] = pd.to_datetime(hoogleraren["Sterfdatum"], errors='coerce')
hoogleraren = hoogleraren.dropna(subset=["Sterfdatum"])
hoogleraren["age"] = (hoogleraren["Sterfdatum"].dt.year - hoogleraren["geboortedatum"].dt.year)
hoogleraren["age"] = hoogleraren["age"].sort_values(ascending=False)
#max age is 100

#test if no negative age when start first start at uni
hoogleraren["Datum aanstelling I"] = pd.to_datetime(hoogleraren["Datum aanstelling I"], errors='coerce')
hoogleraren = hoogleraren.dropna(subset=["Datum aanstelling I"])
hoogleraren["difference"] = (hoogleraren["Datum aanstelling I"].dt.year - hoogleraren["geboortedatum"].dt.year)

#print(sorted(hoogleraren["age"].to_list()))
#print(hoogleraren["age"].sort_values())
print(hoogleraren.groupby(["Achternaam"]).count().sort_values(by=['ID']))
#print(hoogleraren["difference"].sort_values())
#rint(hoogleraren.shape)
