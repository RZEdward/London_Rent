import requests
from bs4 import BeautifulSoup
import re
import statistics
import time
import matplotlib.pyplot as plt
import csv
import numpy as np
import scipy.stats as sts

# Base URL of the SpareRoom search results
base_url = 'https://www.spareroom.co.uk/flatshare/index.cgi'

borough = ['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley', 'Camden', 'City of London', 'Croydon', 'Ealing', 'Enfield', 'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Haringey', 'Harrow', 'Havering', 'Hillingdon', 'Hounslow', 'Islington', 'Kensington and Chelsea', 'Kingston upon Thames', 'Lambeth', 'Lewisham', 'Merton', 'Newham', 'Redbridge', 'Richmond upon Thames', 'Southwark', 'Sutton', 'Tower Hamlets', 'Waltham Forest', 'Wandsworth', 'Westminster']

boroughs = ['1253681945', '1253682990', '1253683109', '1253683193', '1253683273', '1253683402', '1253683532', '1253683619', '1253683686', '1253683782', '1253683856', '1253683920', '1253683967', '1253684019', '1253684084', '1253684187', '1253684263', '1253684618', '1253684688', '1253684747', '1253684818', '1253684877', '1253684949', '1253685010', '1253685064', '1253685123', '1253685179', '1253685262', '1253685306', '1253685428', '1253685485', '1253685531', '1253685570']

master_list = [] # list of lists of rental prices in each borough

stats = [] # list of lists of the stats ( min, max, median, std.dev in each borough )

#-----------------------------------------------------------------------------------

count = 0   # counts number of properties

iteration = 0  # stores borough index

for search_id in boroughs:

    print(borough[iteration])

    # Create an empty list to store the scraped rental prices for this borough
    list = []

    params = {
            'offset': 0,
            'search_id': search_id,
            'sort_by': 'price_low_to_high',
            'mode': 'list'
        }

    response = requests.get(base_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

    # pull the search results header to find total listings
    results_header = soup.find('p', id='results_header').get_text(strip=True)

    # breaking apart the header
    sol = results_header[13:]
    total_results = int(sol[:-7])

    # convert total search results to number of pages to be iterated through
    total_pages = total_results//10 + 1

    for page in range(total_pages):
        # Calculate the offset for the current page (offset in the URL defines results 1-10, 21-30 etc.)
        offset = page * 10
        
        # Define the parameters for the request URL
        params = {
            'offset': offset,
            'search_id': search_id,
            'sort_by': 'price_low_to_high',
            'mode': 'list'
        }

        # Send an HTTP GET request with the updated URL parameters
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # identify listing prices
            rental_cost_elements = soup.find_all('strong', class_='listingPrice')

            # extract listing prices (if range given eg 450-600pcm - take 450)
            for i in range(0, len(rental_cost_elements), 2):
                rental_cost_element = rental_cost_elements[i]
                rental_cost_text = rental_cost_element.get_text(strip=True)
                rental_cost_value = rental_cost_text.split()[0]  # Assuming the value is the last part of the text
                
                if '-' not in rental_cost_value:
                    list.append(rental_cost_value)
                    # now we have a list like [ £300pcm, £100pw, £500pcm]

        else:
            print(f'Failed to retrieve page {page + 1}. Status code:', response.status_code)

    # Now, numeric_values contains the rental prices from all pages, excluding values with hyphens
    cleaned_values = []

    for item in list:
        # Remove unwanted characters and symbols
        cleaned_value = ''.join(char for char in item if char.isdigit() or char == '.')

        # Check if 'pw' is present and adjust weekly rent to monthly
        if 'pw' in item:
            cleaned_value = float(cleaned_value) * (52/12)
        else:
            cleaned_value = float(cleaned_value)

        # Append the cleaned and adjusted value as a number to the new list
        cleaned_values.append(round(cleaned_value, 2))

    # excluding listings described as (4000pcm 4bed - 1000pcm equivalent as only 4000 is registered - with more time I would scrape the number of beds and divide)
    #rental_prices = []
    #for i in range(0, len(cleaned_values)-1):
        #if cleaned_values[i] < 1.5*cleaned_values[i+1]:
            #rental_prices.append(cleaned_values[i])
    #if cleaned_values[-1] < 1.5*cleaned_values[-2]:
        #rental_prices.append(cleaned_values[-1])
    rental_prices = cleaned_values

    master_list.append(rental_prices)

    # find stats of rental_prices in iterated borough
    max_value = max(rental_prices)
    min_value = min(rental_prices)
    median_value = round(np.median(rental_prices),2)
    mean_value = round(np.mean(rental_prices),2)
    stnd_devtn = round(np.std(rental_prices),2)
    q1 = round(np.percentile(rental_prices, 25),2)
    q3 = round(np.percentile(rental_prices, 75),2)
    properties = len(rental_prices)
    stat = [properties, min_value, max_value, median_value, mean_value, stnd_devtn, q1, q3]

    stats.append(stat)

    count += properties

    iteration += 1

    time.sleep(3)

# end borough loop

# convert master list to a flat list to operate stats functions on
flat_list = [item for sublist in master_list for item in sublist]

city_count = count
city_max = max(flat_list)
city_min = min(flat_list)
city_median = statistics.median(flat_list)
city_mean = round(statistics.mean(flat_list),2)
city_stdev = round(statistics.stdev(flat_list),2)
city_q1 = round(np.percentile(flat_list, 25),2)
city_q3 = round(np.percentile(flat_list, 75),2)


city_stats = [count, city_min, city_max, city_median, city_mean, city_stdev, city_q1, city_q3]

csv_file_borough_stats = 'borough_stats.csv'
# headers - count, min, max, median, mean, stdev, q1, q3
# content - [stats[i]]
with open(csv_file_borough_stats, 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Borough', 'Properties', 'Min', 'Max', 'Median', 'Mean', 'Standard Deviation', 'Lower Quartile', 'Upper Quartile'])

    for i in range(len(borough)):
        entry = [borough[i]] + stats[i]
        writer.writerow(entry)
    
    total = ['Total'] + city_stats
    writer.writerow(total)

csv_file_prices = 'prices.csv'

with open(csv_file_prices, 'w', newline='') as file1:
    writer = csv.writer(file1)
    writer.writerow(['Borough', 'Price'])
    for i in range(len(master_list)):
        for j in range(len(master_list[i])):
            entry = [borough[i], master_list[i][j]]
            writer.writerow(entry)


# earlier EDA - check for any obvious errors

#xs = borough
#ys = []
#for i in range(len(stats)):
    #ys.append(stats[i][3])

#plt.barh(xs,ys)
#plt.show()+