import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

users = pd.read_csv('../data/reviews.csv').drop_duplicates(subset='reviewUser')['reviewUser']
print(str(users.count()))
columns = ["user" , "vehicleType", "premium"]
df = pd.DataFrame(columns=columns)
# Initialize an empty list to store DataFrames for each iteration
dfs = []

for user in users:
    try:
        print(' user : ' + str(user) )
        reviewContent = requests.get(
            'https://park4night.com/en/user/' + user )
        soup = BeautifulSoup(reviewContent.text , 'html')
        vehicleType = soup.find("img" , {"class": "me-2 account-avatar-vehicule"} )['src']
        premium = soup.find("img" , {"class": "me-2 account-avatar-premium"} )['src']
        row_df = pd.DataFrame({
        "user": user,
        "vehicleType": [vehicleType],
        "premium": [premium]
        })

        # Append the DataFrame to the list
        dfs.append(row_df)
    except (AttributeError, TypeError):
        pass

# Concatenate all DataFrames in the list along rows
df = pd.concat(dfs, ignore_index=True)

df['vehicleType'].fillna("NaN", inplace=True)
df['premium'].fillna("NaN", inplace=True)


# Replace values based on conditions
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_ul.', na=False), 'Minivan', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_gv.', na=False), 'Camper GV', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_nc.', na=False), 'Not defined', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_v.', na=False), 'Furgoneta', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_pl.', na=False), 'Heavy Van', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_p.', na=False), 'Perfil Van', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_c.', na=False), 'Capuchina Van', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_i.', na=False), 'Integral Van', df['vehicleType'])
df['vehicleType'] = np.where(df['vehicleType'].str.contains('vehicule_4x.', na=False), '4x4', df['vehicleType'])

df['premium'] = np.where(df['premium'].str.contains('badge_none', na=False), '0', df['premium'])
df['premium'] = np.where(df['premium'].str.contains('badge_premium', na=False), '1', df['premium'])


df.to_csv('../data/users.csv', index=False)