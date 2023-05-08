from requests import get
from bs4 import BeautifulSoup
from re import compile
from dataclasses import dataclass


@dataclass
class Listing:
    def __init__(self, href: str, logger=None) -> dict():
        self.url = href
        title_regex = compile(r'<h1[^>]*>"(.*?)"</h1>')
        addr_regex = compile(r'<div[^>]*>([^<]+)</div>')
        prices_regex = compile(r'<span[^>]*>€ ([^<]+)</span>')
        area_rooms_regex = compile(r'<div[^>]*>\s*<span[^>]*>(\d+(?:,\d+)?)</span>')

        soup = BeautifulSoup(get(href).text, 'html.parser')

        self.title = title_regex.search(str(soup.find('h1',
                                                      {'data-testid': 'ad-detail-header'}))).group(1)
        self.area = float(area_rooms_regex.search(str(soup.find('div',
                                                          {'data-testid': 'ad-detail-teaser-attribute-0'}))).group(1))
        self.rooms = int(area_rooms_regex.search(str(soup.find('div',
                                                           {'data-testid': 'ad-detail-teaser-attribute-1'}))).group(1))
        self.price = int(prices_regex.search(str(soup.find('span',
                                                      {'data-testid': 'contact-box-price-box-price-value-0'}))).group(1))
        self.kaution = int(prices_regex.search(str(soup.find('span',
                                                        {'data-testid': 'price-information-freetext-attribute-value-1'}))).group(1))
        self.address = addr_regex.search(str(soup.find('div',
                                                       {'data-testid': 'object-location-address'}))).group(1)
        
        
        # TODO images
        # TODO description
        # self.images_bytes = ...
        # self.description = ...
        try:
            logger.info(self.__repr__())
        except:
            pass
    
    def __eq__(self, obj) -> bool:
        return (self.title == obj.title and self.url == obj.url)

def get_photo(url):
    req = get(url)
    if req.status_code == 200:
        return req.raw
    else:
        return None
    

def init_titles_file(file_path): 
    titles = set()
    with open(file_path,'a') as titles_file:
        for line in titles_file:
            titles.add(Listing(line))
    return titles