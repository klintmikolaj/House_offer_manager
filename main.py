import re
import time
import requests
from dataclasses import dataclass
from collections import OrderedDict


@dataclass(frozen=True) # Unchangeable dataclass
class Offer:
    price: int
    street: str
    room_count: int
    price_per_m2: int
    district: str
    add_date: str

    def __str__(self):
        return f"price: {self.price}, street: {self.street}, room_count: {self.room_count}, price_per_m2: {self.price_per_m2}, district: {self.district}, add_date: {self.add_date}"

    def to_db(self):
        return "INSERT INTO offers (price, street, room_count, price_per_m2, district, add_date) VALUES (%s, %s, %s, %s, %s, %s)" % (
        self.price, self.street, self.room_count, self.price_per_m2, self.district, self.add_date)


test_offer = Offer(100, "test", 2, 100, "test", "test")
print(test_offer)
print(test_offer.to_db())

offer_list = []


def get_page_and_scrape_data(offer_url):
    try:
        with requests.session() as session:
            session.headers = headers
            response = session.get(offer_url, timeout=25)
        price = re.search(r'(?<=,"Price":)(\d+)', response.text).group(1)
        street = re.search(r'({"street":{"id":"\d*","code":"","name":")(.+?)(?=")', response.text).group(2)
        room_count = re.search(r'(?<="numberOfRooms":)(\d+)', response.text).group(1)
        price_per_m2 = re.search(r'(?<="key":"price_per_m","value":")(\d+)', response.text).group(1)
        district = re.search(r'(district":{"id":"\d*","code":")(.+?)(?=")', response.text).group(2)
        add_date = re.search(r'(?<=,"createdAt":")(.+?)(?=")', response.text).group(1)

        # test print
        print("url: ", offer_url)
        print("price: ", price)
        print("street: ", street)
        print("room_count: ", room_count)
        print("price_per_m2: ", price_per_m2)
        print("district: ", district)
        print("add_date: ", add_date)
        print("\n ")
        offer_list.append(Offer(price, street, room_count, price_per_m2, district, add_date))
    except Exception as e:
        print(e)
        print("url: ", offer_url)
        print("\n ")


domain = "https://www.otodom.pl"
headers = OrderedDict([('Accept',
                        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
                       ('Accept-Encoding', 'gzip, deflate, br'),
                       ('Accept-Language',
                        'pl,pl-PL;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6'),
                       ('Cache-Control', 'max-age=0'),
                       ('Dnt', '1'),
                       ('Sec-Ch-Ua',
                        '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'),
                       ('Sec-Ch-Ua-Mobile', '?0'),
                       ('Sec-Ch-Ua-Platform', '"Windows"'),
                       ('Sec-Fetch-Dest', 'document'),
                       ('Sec-Fetch-Mode', 'navigate'),
                       ('Sec-Fetch-Site', 'none'),
                       ('Sec-Fetch-User', '?1'),
                       ('Upgrade-Insecure-Requests', '1'),
                       ('User-Agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')])

session = requests.session()
url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing&page=1&by=LATEST&direction=DESC"
session.headers = headers
response = session.get(url, timeout=25)
#print(response.text)

results = re.findall(r'(?<=<a data-cy="listing-item-link" href=")(.+?)(?=")', response.text)
#print(len(results))

#print("\n".join(map(lambda x: domain + x, results)))
# remove first 3 proposed elements
print("-" * 100)
results = results[3:]

for result in results:
    get_page_and_scrape_data(domain + result)
    # time.sleep(5)

for offer in offer_list:
    print(offer)
    print(offer.to_db())
    print("\n")