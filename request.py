import requests
from bs4 import BeautifulSoup
import json

def get_json_listings(session : requests.Session) :
    base_site = session.get('https://www.willhaben.at/iad/immobilien/mietwohnungen/wien?sort=7&rows=30')

    token = ""

    for i in base_site.headers['set-cookie'].split(';'):
        if i.startswith('Secure, x-bbx-csrf-token'):
            token = i[i.index("=")+1:]

    soup = BeautifulSoup(base_site.text, 'html.parser')
    soup = soup.find('a', {'id' : 'navigator-title-province-Wien'})

    sfId = soup['href'][soup['href'].index("sfId=")+5 : soup['href'].index('&isN')]

    # regex_sfid = re.compile(r'sfId=([\w-]+)')
    # sfId = regex_sfid.search(str(t)).group(1)

    number_of_rows = 200
    json_req = session.get(f'https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/mietwohnungen/wien?sort=7&sfId={sfId}&isNavigation=true&page=1&rows={number_of_rows}', headers={
        'accept': 'application/json',
        'x-bbx-csrf-token': token,
        'x-wh-client': 'api@willhaben.at;responsive_web;server;1.0.0;desktop'
    })
    
    #print(token,'\n')
    #print(sfId,'\n')
    
    if json_req.status_code == 200:
        return json.loads(json_req.text)["advertSummaryList"]['advertSummary']
    else:
        raise Exception('Cant get json from a request')


def get_tuple_listings(filtered_json):
    tuples = set()
    for each in filtered_json:
        uri = each['contextLinkList']['contextLink'][-1]['uri']
        title = each["description"]
        tuples.add((uri,title))
    return tuples
