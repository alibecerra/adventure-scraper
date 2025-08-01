import scrapy
from tabulate import tabulate
import re

class TripSpider(scrapy.Spider):
    name = "trip_spider"
    start_urls = ["https://www.csusb.edu/recreation-wellness/adventure/trips/all-trips-date"]

    def parse(self, response):
        event_links = response.css("a.event--title::attr(href)").getall()
        for link in event_links:
            event_id = re.search(r'/event/(\d+)', link).group(1) if re.search(r'/event/(\d+)', link) else None
            if event_id:
                yield response.follow(f"https://www.csusb.edu/event/{event_id}", callback=self.parse_event)

    def parse_event(self, response):
        fusion_button_link = response.css('a.btn.btn-primary.btn-solid::attr(href)').get()
        if fusion_button_link:
            yield response.follow(fusion_button_link, callback=self.parse_fusion)
        else:
            yield {
                'title': response.css('h1.event--title::text').get().strip() if response.css('h1.event--title::text').get() else "Title Not Found",
                'date': response.css('div.event--date::text').get().strip() if response.css('div.event--date::text').get() else "Date Not Found",
                'spots_left': None
            }

    def parse_fusion(self, response):
        spots_text = response.css('div.spots-tag p.card-text::text').get()
        spots_left = None
        if spots_text:
            match = re.search(r'(\d+) spot(?:s)? left', spots_text, re.IGNORECASE)
            if match:
                spots_left = int(match.group(1))
            else:
                match = re.search(r'Only (\d+) spot(?:s)?', spots_text, re.IGNORECASE)
                if match:
                    spots_left = int(match.group(1))
                elif "Full" in spots_text:
                    spots_left = 0
                else:
                    spots_left = None

        yield {
            'title': response.css('nav[aria-label="breadcrumb"] li:last-child::text').get().strip() if response.css('nav[aria-label="breadcrumb"] li:last-child::text').get() else "Title Not Found",
            'date': response.css('div.event--date::text').get().strip() if response.css('div.event--date::text').get() else "Date Not Found",
            'spots_left': spots_left
        }

    def closed(self, reason):
        items = list(self.crawler.spider.crawler.engine.slot.inprogress)
        if items:
            data = [[item['title'], item['date'], item['spots_left']] for item in items[0]]
            data.insert(0, ["Trip Name", "Trip Date", "Spots Left"])
            print(tabulate(data, headers="firstrow", tablefmt="grid"))
