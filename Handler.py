import re
import requests
from collections import OrderedDict
from Core import get_page_and_scrape_data

domain = "https://www.otodom.pl"
headers = OrderedDict([('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
                       ('Accept-Encoding', 'gzip, deflate, br'),
                       ('Accept-Language', 'pl,pl-PL;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6'),
                       ('Cache-Control', 'max-age=0'),
                       ('Dnt', '1'),
                       ('Sec-Ch-Ua', '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'),
                       ('Sec-Ch-Ua-Mobile', '?0'),
                       ('Sec-Ch-Ua-Platform', '"Windows"'),
                       ('Sec-Fetch-Dest', 'document'),
                       ('Sec-Fetch-Mode', 'navigate'),
                       ('Sec-Fetch-Site', 'none'),
                       ('Sec-Fetch-User', '?1'),
                       ('Upgrade-Insecure-Requests', '1'),
                       ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')])

session = requests.session()
url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing&page=1&by=LATEST&direction=DESC"
session.headers = headers
response = session.get(url, timeout=25)

#Second part of a link added to "https://www.otodom.pl"
results = re.findall(r'(?<=<a data-cy="listing-item-link" href=")(.+?)(?=")', response.text)

# remove first 3 proposed elements
results = results[3:]

for result in results:
    get_page_and_scrape_data(domain + result, headers)
    time.sleep(5)






