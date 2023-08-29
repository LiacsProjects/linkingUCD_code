from geopy.geocoders import Nominatim
import geocoder
import pandas as pd
import data


def generate_coords():
    death_cities_prof = list(set(data.individual_profs_df['Death place']))
    birth_cities_prof = list(set(data.individual_profs_df['Birth place']))
    cities_student = list(set(data.individual_student_df['City']))
    list_of_cities = list(set(death_cities_prof + birth_cities_prof + cities_student))

    geolocator = Nominatim(user_agent="Geopy_app")
    coordinates = []
    for row in list_of_cities:
        try:
            location = geolocator.geocode(row)
            coordinates.append((location.raw['lat'], location.raw['lon']))
        except:
            coordinates.append(None)

    coords_df = pd.DataFrame(
        {'City': list_of_cities,
         'Coordinates': coordinates
         })

    latitudes = []
    longitudes = []
    for row in coords_df['Coordinates']:
        try:
            row = row.replace(',', '')
            row = row.replace("'", '')
            row = row.replace('(', '')
            row = row.replace(')', '')
            row = row.split(' ')
            latitudes.append(row[0])
            longitudes.append(row[1])
        except:
            latitudes.append(None)
            longitudes.append(None)
    coords_df['Latitudes'] = latitudes
    coords_df['Longitudes'] = longitudes
    coords_df.to_excel('Birth_place_coords.xlsx')
    print('done with birth')


generate_coords()