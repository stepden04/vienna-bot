from requests import get
from bs4 import BeautifulSoup
from dataclasses import dataclass
from html2text import html2text

@dataclass
class Listing:
    
    title : str
    uri : str
    area : str
    rooms : str
    price : str
    kaution : str
    address : str
    description : str
    
    def __init__(self, uri: str, title: str) -> dict():
        self.uri = uri
        self.title = title

        self.get_data_from_listings(get(uri).text)

    def __eq__(self, obj) -> bool:
        return (self.title == obj.title and self.url == obj.url)

    def get_data_from_listings(self, listing_text):
        soup = BeautifulSoup(listing_text, 'html.parser')

        self.area = str(soup.find('div',
                                  {'data-testid': 'ad-detail-teaser-attribute-0'}))
        self.area = self.area[self.area.index(r'QY">')+4 : self.area.index("</span>")]

        
        self.rooms = str(soup.find('div',
                                   {'data-testid': 'ad-detail-teaser-attribute-1'}))
        self.rooms = self.rooms[self.rooms.index(r'QY">')+4 : self.rooms.index("</span>")]


        self.price = str(soup.find('span',
                                   {'data-testid': 'contact-box-price-box-price-value-0'}))
        self.price = self.price[self.price.index(r'value-0">')+9 : self.price.index("</span>")].replace(' ','')
        

        self.kaution = str(soup.find('span',
                                     {'data-testid': 'price-information-freetext-attribute-value-1'}))
        self.kaution = self.kaution[self.kaution.index(r'value-1">')+9 : self.kaution.index("</span>")].replace(' ','')


        self.address = str(soup.find('div',
                                     {'data-testid': 'object-location-address'}))
        self.address = self.address[self.address.index(r'address">')+9 : self.address.index("</div>")]


        self.description = str(soup.find('div',
                                         {'data-testid': 'ad-description-Objektbeschreibung'}))
        self.description = html2text(self.description[self.description.index(
            r'Objektbeschreibung">'): self.description.index(r'</div>')])
