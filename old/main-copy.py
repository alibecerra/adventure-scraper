from bs4 import BeautifulSoup
import re
import requests
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor

main_page = "https://www.csusb.edu/recreation-wellness/adventure/trips/all-trips-date"
base_url = "https://www.csusb.edu"

response = requests.get(main_page)
soup = BeautifulSoup(response.text, 'html.parser')

list_of_href = soup.find_all('a', href=True)
pattern = re.compile(r'\/event\/\d{5,6}')

href_trips = []

for i in list_of_href:
    match = re.search(pattern, str(i))
    if match:
        href_trips.append(match.group())

def fetch_trip_info(page):
    trip = requests.get(base_url + page)
    # print(base_url + page)
    trip_soup = BeautifulSoup(trip.text, 'html.parser')
    trip_date = trip_soup.find('div', class_="event--date").text
    trip_name = trip_soup.find('h2', class_="event--title").text
    fusion_button = trip_soup.find('a', class_="btn btn-primary btn-solid")
    
    # print(fusion_button)

    if (fusion_button is not None) and (len(fusion_button.get('href')) == 145):
        trip_spots = requests.get(fusion_button.get('href'))
        # print(trip_spots)
        fusions_page = BeautifulSoup(trip_spots.text, 'html.parser')
        # print(fusions_page)
        spots_left = fusions_page.find('p', class_="card-text").text
        print(spots_left)
    else:
        spots_left = "0 spot(s)"
    
    return [trip_name, trip_date, spots_left]

# Using ThreadPoolExecutor to fetch trip info concurrently
with ThreadPoolExecutor(max_workers=16) as executor:
    scraped_data = list(executor.map(fetch_trip_info, href_trips))

# Insert header row
scraped_data.insert(0, ["Trip Name", "Trip Date", "Spots left"])

# Print the tabulated data
table = tabulate(scraped_data, headers="firstrow", tablefmt="grid")
print(table)
