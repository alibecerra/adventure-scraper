from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

main_page = "https://www.csusb.edu/recreation-wellness/adventure/trips/all-trips-date"
base_url = "https://www.csusb.edu"

def gathering():

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

    return href_trips
        
def gather_to_output(href_trips):
    sign_up_button = []
    spots_left = 0
    scraped_data = [["Trip Name", "Trip Date", "Spots left"]]

    for page in href_trips:

        program_id = trip_soup.find('input',{'id':'ProductId'}).text
        semester_id = trip_soup.find('input',{'id':'DefaultSemesterId'}).text

        querystring = {f"semesterId": semester_id,
                   f"programId": program_id}
        
        payload = ""

        headers = {"cookie": "ASP.NET_SessionId=mwucyrxvhltyzu14ylv5kwhs; __RequestVerificationToken=qDm0s90xP-P2qjIOe5ur3jqvkUN3cb7vI0U3ScIFqDIbcQJVgg0PPhLVr0DjDtp9hUPNjnN6rYZgTwVFZqkwLzFUWl8C6d1SeKKgbcEwOzA1"}

        trip = requests.request("GET", url, data=payload, headers=headers, params=querystring)
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
                spots_left = fusions_page.find('p', class_="car-text").text[:-9]
        
        scraped_data.append([trip_name, trip_date, spots_left])
    
    return scraped_data




trips_list_crawled = gathering()
output = gather_to_output(trips_list_crawled)
print(output)