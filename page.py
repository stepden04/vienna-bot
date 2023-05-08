from requests import get
from bs4 import BeautifulSoup
import re


def get_data_from_page(href: str, logger=None) -> dict():
    """_summary_

    Args:
        href (str, logger(optional)): _description_. Defaults to None)->dict(.
        Link to a listing page
    Returns:
        Dictionary of title,price etc from a webpage
    """
    title_regex = re.compile(r'<h1[^>]*>"(.*?)"</h1>')
    addr_regex = re.compile(r'<div[^>]*>([^<]+)</div>')
    price_regex = re.compile(r'<span[^>]*>€ ([^<]+)</span>')
    area_rooms_regex = re.compile(r'<div[^>]*>\s*<span[^>]*>(\d+(?:,\d+)?)</span>')

    listing_dict = dict()

    soup = BeautifulSoup(get(href).text, 'html.parser')

    # TODO add regex
    title = title_regex.search(str(soup.find('h1',
                          {'data-testid': 'ad-detail-header'}))).group(1)
    area = area_rooms_regex.search(str(soup.find('div',
                         {'data-testid': 'ad-detail-teaser-attribute-0'}))).group(1)
    rooms = area_rooms_regex.search(str(soup.find('div',
                          {'data-testid': 'ad-detail-teaser-attribute-1'}))).group(1)
    price = price_regex.search(str(soup.find('span',
                          {'data-testid': 'contact-box-price-box-price-value-0'}))).group(1)
    kaution = price_regex.search(str(soup.find('span',
                            {'data-testid': 'price-information-freetext-attribute-value-1'}))).group(1)
    address = addr_regex.search(str(soup.find('div',
                                {'data-testid': 'object-location-address'}))).group(1)
    # imgs = set(...))

    listing_dict.update(title=title, area=area, rooms=rooms,
                        price=price, kaution=kaution, address=address)

    try:
        for val in listing_dict.values():
           print(val, '\n')
    except:
        pass

    return listing_dict

# TODO images

def get_images(links: set()):
    images = set()

    for link in links:
        images.add(get(link))

    return images
