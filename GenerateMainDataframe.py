import pandas as pd
import os

# Convert JSON to DataFrame Using read_json()


parent_folder = 'data/generated'
dfs = []

for subfolder in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, subfolder)

    if os.path.isdir(subfolder_path):  # Check if it's a subfolder
        for filename in os.listdir(subfolder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(subfolder_path, filename)

                # Load the JSON file into a DataFrame and append it to the list
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json_file.read()
                    df = pd.read_json(data)
                    dfs.append(df)

converted_df = pd.concat(dfs, ignore_index=True)

#Delete multiple occurences with same id
final = converted_df.drop_duplicates(subset='id')
df_sorted = final.sort_values(by='id', ascending=True)

# Display the counts
print(df_sorted.head())

df_sorted.to_csv('data/ibericMainData.csv', index=False)
