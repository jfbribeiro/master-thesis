import pandas as pd
import csv
import requests
import os


df = pd.read_csv('../data/worldcities.csv')
iberic_countries = df[(df["country"] == "Portugal") | (df["country"] == "Spain")]
iberic_countries['lat'] = iberic_countries['lat'].astype(str).str.replace(',', '.')
iberic_countries['lng'] = iberic_countries['lng'].astype(str).str.replace(',', '.')

# Iterate over each row in the DataFrame
for index, row in iberic_countries.iterrows():
    latitude = row['lat']
    longitude = row['lng']
    city_name = row['city']
    country = row['country']

    # Determine the folder based on the country
    folder = 'data/generated/Portugal' if country == 'Portugal' else 'data/generated/Spain'

    # Define the API URL with parameters
    api_url = f'https://park4night.com/api/places/around?lat={latitude}&lng={longitude}&radius=200&filter=%7B%7D&lang=en'

    # Make a GET request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Store the API response in a file with the city name in the appropriate folder
        with open(os.path.join(folder, f'{city_name}.json'), 'w') as file:
            file.write(response.text)
    else:
        print(f"Failed to retrieve data for {city_name} in {country}")