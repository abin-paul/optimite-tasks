import requests
import json
from pprint import pprint

def sent_request(url):
	"""
        Send a GET request to the specified URL and return the ouput
	"""
	headers = {
		'Cache-Control': 'no-cache',
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	response = requests.request("GET", url, headers=headers)
	data = json.loads(response.text)
	return data

def get_cats_weight_average():
    cats_api = sent_request('https://api.thecatapi.com/v1/breeds')

    whole_weight = 0
    number_of_cats = 0

    # Iterate through the data to calculate total weight and count of cats
    for cat in cats_api:
        weight_metric = cat['weight']['metric'].split(' - ')
        weight_metric_avg = (int(weight_metric[0]) + int(weight_metric[1])) / 2
        whole_weight += weight_metric_avg
        number_of_cats += 1

    # Calculate the average weight
    average_weight = whole_weight / number_of_cats

    return average_weight

def get_country_data():
    countries_api = sent_request('https://restcountries.com/v2/all')

    
    n = len(countries_api)
    #sorting the countries by area
    for i in range(n):
        for j in range(0, n-i-1):
            if countries_api[j].get('area', 0) < countries_api[j+1].get('area', 0):
                countries_api[j], countries_api[j+1] = countries_api[j+1], countries_api[j]

    unique_languages = set()
    # Iterate through the data and add languages to the set
    for country in countries_api:
        languages = country.get('languages', [])
        for lang in languages:
            unique_languages.add(lang['name'])

    return countries_api[:10], len(unique_languages)


print("--------------Task 4-----------")
print("------Top 10 Countries---------")
top_10_countries, number_unique_langs = get_country_data()
cat_average_weight = get_cats_weight_average()
for country in top_10_countries:
    print(country['name'], country['area'])
print("------------------------")
print("------Total number of languages in the world used as officials---------")
print(f"Total unique languages: {number_unique_langs}")
print("------------------------")
print("------the average weight of cat in metric unit---------")
print(f"The average weight: {cat_average_weight}")
print("--------------End Task 4-----------")
