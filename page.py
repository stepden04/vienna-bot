from requests import get
from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.request import urlretrieve


@dataclass(frozen=True, slots=True)
class Listing:
    url: str
    title: str
    description: str
    address: str
    rooms: str
    price: str
    kaution: str
    area: str
    images_links: set

    def compose(self):
        return f'{self.title}' \
               f'\n{self.address}\t{self.rooms}rooms/{self.area}m²' \
               f'\n{self.description}' \
                   f'\nPrice: €{self.price} + Kaution: €{self.kaution}'


def init_titles_file(file_path):
    titles = set()
    with open(file_path, 'a') as titles_file:
        for line in titles_file:
            titles.add(Listing(line))
    return titles
