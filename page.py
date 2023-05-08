from requests import get
from bs4 import BeautifulSoup


def get_data_from_page(href: str, logger=None) -> dict():
    """_summary_

    Args:
        href (str, logger(optional)): _description_. Defaults to None)->dict(.
        Link to a listing page
    Returns:
        Dictionary of title,price etc from a webpage
    """
    listing_dict = dict()

    soup = BeautifulSoup(get(href).text, 'html.parser')

    # TODO add regex
    title = str(soup.find('h1',
                          {'data-testid': 'ad-detail-header'}))
    area = str(soup.find('div',
                         {'data-testid': 'ad-detail-teaser-attribute-0'}))
    rooms = str(soup.find('div',
                          {'data-testid': 'ad-detail-teaser-attribute-1'}))
    price = str(soup.find('span',
                          {'data-testid': 'contact-box-price-box-price-value-0'}))
    kaution = str(soup.find('span',
                            {'data-testid': 'price-information-freetext-attribute-label-1'}))
    address = str(soup.find_all('div',
                                {'data-testid': 'object-location-address'}))
    # imgs = set(...))

    listing_dict.update(title=title, area=area, rooms=rooms,
                        price=price, kaution=kaution, address=address)

    try:
        for val in listing_dict.values():
            logger.info(val, '\n')
    except:
        pass

    return listing_dict


def get_images(links: set(str)):
    images = set()

    for link in links:
        images.add(get(link))

    return images
