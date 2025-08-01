import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

URL = "https://www.csusb.edu/recreation-wellness/adventure/trips/all-trips-date"

def get_trips():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    trips = []
    
    # Updated selector to find the main content container
    main_content = soup.find('article') or soup.find('div', class_='content')
    
    if not main_content:
        raise ValueError("Could not find trip content section - website structure may have changed")
    
    # Look for trip items using more specific selectors
    trip_items = main_content.find_all(['li', 'div'], class_=lambda x: x and 'trip' in x.lower())
    
    for item in trip_items:
        try:
            text = item.get_text(strip=True, separator=' ')
            parts = [p.strip() for p in text.split('- SBC') if p.strip()]
            
            if len(parts) < 2:
                continue
                
            date_str, name = parts[0], parts[1]
            current_year = datetime.now().year
            
            # Parse date with year handling
            start_date = datetime.strptime(f"{date_str} {current_year}", "%b %d %Y")
            end_date = datetime.strptime(f"{date_str} {current_year}", "%b %d %Y")
            
            trips.append({
                'name': name,
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d"),
                'spots_available': 'Check website'  # Still not publicly listed
            })
            
        except Exception as e:
            print(f"Error processing item: {e}")
            continue
            
    return trips

try:
    with open('csusb_trips.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'start_date', 'end_date', 'spots_available']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(get_trips())
    print("Successfully created CSV file")
except Exception as e:
    print(f"Error: {e}")
    print("Tip: Check if the CSUSB trips page structure has changed")
