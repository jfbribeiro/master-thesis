# Master Thesis
This repository will be used during the academic year 2023/2024 to develop my master thesis.

As a first step, and to get all the relevant data, I scraped park4night website to obtain all the parking spots and existing reviews in the Iberian Peninsula.
Park4Night website itself is really complicated to scrap for the parking spots, as the map only renders a small amount of places independently of the size area you select the explore. With these restrictions, i started exploring and found an API service from them where you can use latitude and longitude and a radius to retrieve all the places around that central spot, so obtaining a dataset with all the coordinates from Portuguese and Spanish cities, it was possibly to iterate them, call the service and fetch all the data about the existing parking spots ensuring that there are no duplicate records in the end.
From there and having the parking spots IDs, plain web scraping was done to get all the reviews in english for all those places obtained previously.

Next step will be to scrap the website to discover the type of vehicle for each user.
