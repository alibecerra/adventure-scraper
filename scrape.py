import requests 
import re
import scrapy
from bs4 import BeautifulSoup



base_url = "https://www.csusb.edu/recreation-wellness/adventure/trips/all-trips-date"
event_url = "https://www.csusb.edu/event/"
event_ids= []
trip_master_matrix = [["Trip Name", "Trip Date", "Spots left"]]


# uses regex to get the event number to use in event_url
def event_num(text):
    match = re.search(r'\d+', text)
    return match.group(0) if match else None

def main_page_scrape(url):
    # request and format html to parse
    response = requests.get(url)
    html_of_page = response.text
    soup = BeautifulSoup(html_of_page, "html.parser")

    # using the base url get the trip date url codes
    links = soup.find_all("a", attrs={'href': True, "class": "event--title"})
    for i in links:
        event_ids.append(event_num(str(i)))
   
def fusion_button_finder(param1=event_ids):
    #using the event_ids list go through every trip and find its fusion button else return null
    fusion_button_list = []
    for i in event_ids:
        r = requests.get(event_url + i)
        page = r.text
        soup = BeautifulSoup(page, "html.parser")
        fus_button = soup.find('a', attrs={'href':True, "class":"btn btn-primary btn-solid"})
        fusion_button_list.append(fus_button)
    return fusion_button_list

def fusion_spots_left(list_of_buttons):


main_page_scrape(base_url)
list_of_fusion = fusion_button_finder()
