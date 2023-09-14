import pandas as pd
import csv
import requests
import os
from bs4 import BeautifulSoup


ibericMainData = pd.read_csv('data/ibericMainData.csv')
columns = ["placeId" , "reviewId", "reviewRate", "reviewUser", "reviewDate", "reviewContent"]
df = pd.DataFrame(columns=columns)

# Initialize an empty list to store DataFrames for each iteration
dfs = []

for index, row in ibericMainData.iterrows():
    rowUrl = row['url']
    placeId = row['id']
    print("Working for " + str(placeId) )
    url = 'https://park4night.com' + rowUrl
    page = requests.get(url)
    soup = BeautifulSoup(page.text , 'html')

    reviews = soup.findAll("article" , {"class": "place-feedback-article"} )
    for review in reviews:
        reviewId = review['data-review-id']
        reviewRate = review['data-review-rating']
        # Initialize variables for user and date
        reviewUser = ""
        reviewDate = ""

        try:
            reviewUser = review.find('header').find('strong').contents[0]
        except (AttributeError, IndexError):
            pass  # Handle the case where the element is not found

        try:
            reviewDate = review.find('header').find('span').contents[0]
        except (AttributeError, IndexError):
            pass  # Handle the case where the element is not found

        #to get the review text in english
        reviewContent = (requests.get('https://park4night.com/services/V4.1/commGetTrad_cors.php?id_comm='+reviewId+'&context_lang=en')).json()['translation']

        # Create a DataFrame for the current row
        row_df = pd.DataFrame({
            "placeId" : placeId,
            "reviewId": [reviewId],
            "reviewRate": [reviewRate],
            "reviewUser": [reviewUser],
            "reviewDate": [reviewDate],
            "reviewContent": [reviewContent]
        })

        # Append the DataFrame to the list
        dfs.append(row_df)

# Concatenate all DataFrames in the list along rows
df = pd.concat(dfs, ignore_index=True)

df.to_csv('data/ibericMainDataComments.csv' , index=False)

