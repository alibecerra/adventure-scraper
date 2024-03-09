from bs4 import BeautifulSoup
import re
import requests
from tabulate import tabulate

main_page = "https://www.csusb.edu/recreation-wellness/adventure/trips/all-trips-date"
base_url = "https://www.csusb.edu"

response = requests.get(main_page)
soup = BeautifulSoup(response.text, 'html.parser')
html = soup.prettify()

list_of_href = soup.find_all('a', href=True)

pattern = re.compile(r'\/event\/\d{5,6}')

href_trips = []

for i in list_of_href:

    match = re.search(pattern, str(i))
    if match:
        href_trips.append(match.group())

sign_up_button = []
scraped_data = [["Trip Name", "Trip Date", "Spots left"]]

for page in href_trips:
    trip = requests.get(base_url + page)
    trip_soup = BeautifulSoup(trip.text, 'html.parser')
    
    trip_date = trip_soup.find('div', class_="event--date").text
    trip_name = trip_soup.find('h2', class_="event--title").text

    fusion_button = trip_soup.find('a', class_="btn btn-primary btn-solid")
    
    if (fusion_button is not None) and (len(fusion_button.get('href')) == 145):
        trip_spots = requests.get(fusion_button.get('href'))
        fusions_page = BeautifulSoup(trip_spots.text, 'html.parser')
        
        if fusions_page.find('p', class_="car-text") is None:
            spots_left = "0 spot(s)"
        else:
            spots_left = fusions_page.find('p', class_="car-text").text
        
    scraped_data.append([trip_name, trip_date, spots_left])

table = tabulate(scraped_data, headers="firstrow", tablefmt="grid")
print(table)