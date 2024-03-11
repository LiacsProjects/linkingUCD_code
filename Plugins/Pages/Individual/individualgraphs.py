
from Plugins.globals import data

def get_unique_values(subject):
    unique_values = data.individual_profs_df[subject].dropna().sort_values().unique()
    unique_values = unique_values.tolist()
    return unique_values
