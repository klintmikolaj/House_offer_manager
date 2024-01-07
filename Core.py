import re
import requests
from dataclasses import dataclass
from collections import OrderedDict
import time
import mysql.connector


@dataclass(frozen=True)  # Unchangeable dataclass
class Offer:
    offer_id: str
    price: int
    street: str
    room_count: int
    price_per_m2: int
    district: str
    add_date: str

    def __str__(self):
        return (f" offer_id: {self.offer_id}, price: {self.price}, street: {self.street}, room_count: {self.room_count}"
                f", price_per_m2: {self.price_per_m2}, district: {self.district}, add_date: {self.add_date}")

    def to_db(self):
        return (
                    "INSERT INTO (offer_id, price, street, room_count, price_per_m2, district, add_date) VALUES (%s, %s, %s, %s, %s, %s, %s)" %
                    (self.offer_id, self.price, self.street, self.room_count, self.price_per_m2, self.district,
                     self.add_date))


class Core:
    def __init__(self):
        self.domain = "https://www.otodom.pl"
        self.offer_list = []  # The list stores dataclass objects
        self.db = mysql.connector.connect(host="localhost", user="root", passwd="eloelo320", database="homes")
        self.db_cursor = self.db.cursor()
        self.headers = OrderedDict()
        self.max_page_id = 10

    def init_headers(self):
        '''Request headers to imitate the web browser'''
        self.headers = OrderedDict([('Accept',
                                     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
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
                                    ('User-Agent',
                                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')])

    def get_page_and_scrape_data(self, offer_url):
        '''Creates a session, gets certain value from get request and appends them to an offer list'''
        try:
            offer_id = offer_url
            with requests.session() as session:
                session.headers = self.headers
                response = session.get(offer_url, timeout=25) # Sending a request to every offer
            if price_match := re.search(r'(?<=,"Price":)(\d+)', response.text):
                price = price_match.group(1)
            else:
                price = [x for x in re.finditer(r'(?<=,"fullNameItems":\[")(.+?)(?=",)', response.text)][-1].group(1)
            if street := re.search(r'({"street":{"id":"\d*","code":"","name":")(.+?)(?=")', response.text):
                street = street.group(2)
            else:
                street = [x for x in re.finditer(r'(?<=,"fullNameItems":\[")(.+?)(?=",)', response.text)][-1].group(1)
            room_count = re.search(r'(?<="numberOfRooms":)(\d+)', response.text).group(1)
            price_per_m2 = re.search(r'(?<="key":"price_per_m","value":")(\d+)', response.text).group(1)
            district = re.search(r'(district":{"id":"\d*","code":")(.+?)(?=")', response.text).group(2)
            add_date = re.search(r'(?<=,"createdAt":")(.+?)(?=")', response.text).group(1)

            self.offer_list.append(Offer(offer_id, price, street, room_count, price_per_m2, district, add_date))

        except Exception as exc:
            pass

        finally:
            print("Adding new object!")


    def get_offer_list(self):
        '''Creates results list filled with offer urls from certain range and scrapes the data from them '''
        for current_page_id in range(1, self.max_page_id + 1):
            session = requests.session()
            url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing&page={current_page_id}by=LATEST&direction=DESC"
            session.headers = self.headers
            response = session.get(url, timeout=25)

            # Second part of a link added to "https://www.otodom.pl"
            results = re.findall(r'(?<=<a data-cy="listing-item-link" href=")(.+?)(?=")', response.text)

            # Remove first 3 proposed elements
            results = results[3:]

            for result in results:
                self.get_page_and_scrape_data(self.domain + result)
                time.sleep(1)

    def create_database(self):
        self.db_cursor.execute("CREATE DATABASE IF NOT EXISTS homes")
        self.db_cursor.execute("USE homes")
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS homes_tb (
                offer_id VARCHAR(500) PRIMARY KEY,
                price INT UNSIGNED,
                street VARCHAR(500),
                room_count SMALLINT UNSIGNED,
                price_per_m2 SMALLINT UNSIGNED,
                district VARCHAR(500),
                add_date DATETIME
            )
        """)
        self.db.commit()

    def upload_to_database(self):
        for offer in self.offer_list:
            self.db_cursor.execute(
                "INSERT IGNORE INTO homes_tb (offer_id, price, street, room_count, price_per_m2, district, add_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    offer.offer_id, offer.price, offer.street, offer.room_count, offer.price_per_m2, offer.district,
                    offer.add_date))
            self.db.commit()

    def run(self):
        self.init_headers()
        self.get_offer_list()
        self.create_database()
        self.upload_to_database()
