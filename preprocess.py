import pandas as pd
import pyreadr
import time


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
    df = pd.read_excel(file_location, engine='openpyxl')  # .replace({np.nan: None})

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

    # Strip unwanted characters from dates
    df['geboortedatum'].replace(regex=True, inplace=True, to_replace=r'[^0-9/\-]', value=r'')
    df['Sterfdatum'].replace(regex=True, inplace=True, to_replace=r'[^0-9/\-]', value=r'')

    # Remove '?' and values between parentheses "()" from places
    df['Geboorteplaats'] = df['Geboorteplaats'].str.replace(r"\([^()]*\)", "", regex=True).str.strip('? ')
    df['Sterfplaats'] = df['Sterfplaats'].str.replace(r"\([^()]*\)", "", regex=True).str.strip('? ')
    # t = []
    # for col in t:
    #     df[col] = df[col].str.title()
    print(f"Hoogleraren data cleaned in {time.time() - start1} seconds")

    # start2 = time.time()
    df.to_excel(r'data/Hoogleraren all - preprocessed.xlsx', index=False)
    # print(f"DataFrame to Excel in {time.time() - start2} seconds")


# For testing only, can be removed if needed
def test():
    file_location = r"data/Hoogleraren all.xlsx"
    df = pd.read_excel(file_location, engine='openpyxl')


# Main
if __name__ == "__main__":
    start = time.time()
    # hoogleraren()
    # standardNamesInit()
    test()
    print(f"Program finished successfully in {time.time() - start} seconds")
