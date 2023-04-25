import numpy as np
import pandas as pd
import pyreadr
import time
import excelAdapter as exad
from datetime import datetime


# Remove empty columns of standardized names
def standardNamesInit():
    relative = r'Standard names/'
    file_locations = [r"standard firstnames.xlsx", r"standard lastnames.xlsx"]
    for file in file_locations:
        df = pd.read_excel(relative + file, engine='openpyxl')
        df.dropna(subset=['standard'], inplace=True)
        df['name'] = df['name'].str.capitalize()
        df['standard'] = df['standard'].str.capitalize()
        df.to_excel(relative + r'short ' + file, index=False)


def RDStoExcel():
    result = pyreadr.read_r('Preprocessed_data/data_wide.RDS')
    RDS_df = result[None]  # extract the pandas data frame
    RDS_df.to_excel(r'Preprocessed_data/data_wide.xlsx', index=False)


def hoogleraren():
    file_location = r"data/Hoogleraren all.xlsx"
    df = pd.read_excel(file_location, engine='openpyxl')  #.replace({np.nan: None})
    # for qq in df['Roepnaam'].head(10):
    #     print(qq, type(qq))
    #     if qq is not np.nan:
    #         print("Hello")
    # return

    start1 = time.time()
    # Standardize countries
    Duitsland = ["Duitsland", "[vermoedelijk  Duitsland]"]
    India = ['India', 'Indië']
    Israel = ["Israel", "Israël"]
    Nederland = ["Nederland", "Nederlan", "Nederlands", "Leiden"]
    Nieuw_Zeeland = ["Nieuw Zeeland", "Nieuw-Zeeland"]
    Rusland = ["Rusland", "USSR"]
    VK = ["Verenigd Koninkrijk", "Verenigde Koninkrijk", "Verenigd Koninkrijk, Engeland",
          "Verenigd Koninkrijk, Schotland", "Engeland", "Schotland", "Verenigd Koninkrijk, Noord-Ierland"]
    VS = ["Verenigde Staten", "USA", "Amerika", "U.S.A."]
    Zwitserland = ["Zwitserland", "Zwitzerland"]
    country_list = [Duitsland, India, Israel, Nederland, Nieuw_Zeeland, Rusland, VK, VS, Zwitserland]
    df['Geboorteland'] = df['Geboorteland'].str.replace(r"\([^()]*\)", "", regex=True).str.strip(' ')
    for c in country_list:
        df['Geboorteland'] = df['Geboorteland'].where(~df['Geboorteland'].isin(c[1:]), c[0])
        df['Land van overlijden'] = df['Land van overlijden'].where(~df['Land van overlijden'].isin(c[1:]), c[0])

    # TODO: inaccurate (1990-01/02 -> 1990-0102, 1909--02?)
    # Strip unwanted characters from dates
    # df['geboortedatum'].replace(regex=True, inplace=True, to_replace=r'[^0-9/\-]', value=r'')
    # df['Sterfdatum'].replace(regex=True, inplace=True, to_replace=r'[^0-9/\-]', value=r'')

    # Remove '?' and values between parentheses "()" from places
    df['Geboorteplaats'] = df['Geboorteplaats'].str.replace(r"\([^()]*\)", "", regex=True).str.strip('? ')
    df['Sterfplaats'] = df['Sterfplaats'].str.replace(r"\([^()]*\)", "", regex=True).str.strip('? ')

    # Check age, if invalid (age > 113 years) remove date of death
    df['geboortedatum'] = df['geboortedatum'].apply(exad.checkDate)
    df['Sterfdatum'] = df['Sterfdatum'].apply(exad.checkDate)
    max_age = 401778
    for ind in df.index:
        if df.loc[ind, "geboortedatum"] is not np.nan and df.loc[ind, "Sterfdatum"] is not np.nan and df.loc[ind, "geboortedatum"] is not None and df.loc[ind, "Sterfdatum"] is not None:
            if (datetime.strptime(df.loc[ind, "Sterfdatum"], "%Y-%m-%d") - datetime.strptime(df.loc[ind, "geboortedatum"], "%Y-%m-%d")).days > max_age:
                df.loc[ind, "Sterfdatum"] = np.nan
    print(f"Hoogleraren data cleaned in {time.time() - start1} seconds")

    # start2 = time.time()
    df.to_excel(r'data/Hoogleraren all - preprocessed.xlsx', index=False)
    # print(f"DataFrame to Excel in {time.time() - start2} seconds")


# For testing only, can be removed if needed
def test():
    dateColumns = ["geboortedatum", "Sterfdatum", "Datum aanstelling I", "Datum aanstelling II",
                   "Datum aanstelling III", "Datum aanstelling IV", "Einde dienstverband I", "Einde dienstverband II",
                   "Einde dienstverband III", "Einde dienstverband IV"]
    file_location = r"data/Hoogleraren all.xlsx"
    df = pd.read_excel(file_location, parse_dates=dateColumns, engine='openpyxl')
    # Check age if possible
    # df['geboortedatum'] = df['geboortedatum'].apply(exad.checkDate)
    # df['Sterfdatum'] = df['Sterfdatum'].apply(exad.checkDate)
    # max_age = 401778
    # for ind in df.index:
    #     if df.loc[ind, "geboortedatum"] is not np.nan and df.loc[ind, "Sterfdatum"] is not np.nan and df.loc[ind, "geboortedatum"] is not None and df.loc[ind, "Sterfdatum"] is not None:
    #         if (datetime.strptime(df.loc[ind, "Sterfdatum"], "%Y-%m-%d") - datetime.strptime(df.loc[ind, "geboortedatum"], "%Y-%m-%d")).days > max_age:
    #             print(datetime.strptime(df.loc[ind, "Sterfdatum"], "%Y-%m-%d"))
    #             df.loc[ind, "Sterfdatum"] = np.nan


# Main
if __name__ == "__main__":
    start = time.time()
    # hoogleraren()
    # standardNamesInit()
    test()
    print(f"Program finished successfully in {time.time() - start} seconds")
