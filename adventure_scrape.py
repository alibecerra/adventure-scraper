import mechanicalsoup
from bs4 import BeautifulSoup
from tabulate import tabulate
import re

browser = mechanicalsoup.StatefulBrowser()
url = "https://recshop.csusb.edu/Program/GetProducts?productTypeCV=00000000-0000-0000-0000-000000003502&classification=7f9e3be9-bc47-443a-86ba-3c7fa4c13bb5"
browser.open(url)
prefix_url = "https://recshop.csusb.edu"

page = browser.page

pattern = r"window\.location='\/Program\/GetProgramDetails\?courseId=[\w-]+&semesterId=[\w-]+'(?=})"
matches = re.findall(pattern, str(page))


trip_list = []

for link in matches:
    trip_page_link = prefix_url + link[17:-1]
    page_link = browser.get(trip_page_link)
    page_link = page_link.content
    page_link_soup = BeautifulSoup(page_link, 'html.parser')

    trip_title = page_link_soup.find('title').text

    if  page_link_soup.find('p', class_="car-text") == None:
        trip_spots = "0 spot(s) available"
    else:
        trip_spots = page_link_soup.find('p', class_="car-text").text

    trip_list.append([trip_title[:-23], int(trip_spots[:-17])])


table = tabulate(sorted(trip_list, key=lambda x: x[1]), tablefmt="grid")
print(table)