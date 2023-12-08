import re
import requests
from dataclasses import dataclass
import time

class Core:
    def __init__(self):
        self.offer_list = [] #lista przechowuje obiekty dataclass
        self.data_base = ... #obiekt MySQL.connector, przechowuje połączenie do bazy danych, zatwierdzamy zmiany w bazie danych
        self.data_base_cursor = ... #wysyłanie query do bazy danych
        self.headers = ...
        self.page_id = ...

    def get_page_and_scrape_data(self, offer_url):
        ...

    def get_offer_list(self):
        ...

    def upload_to_database(self):
        ...

    def run(self):
        ...
    ''' wyciagaj liste ofert z zakladek, dla kazdej z ofert wywolaj getandscrapt, jak sie wypelni lista, connect to db, wywolaj metode upload to database'''

    def connect_database(self):
        ...
    ''' laczy sie z baza  '''



def get_page_and_scrape_data(offer_url, headers):
    try:
        with requests.session() as session:
            session.headers = headers
            response = session.get(offer_url, timeout=25)
        price = re.search(r'(?<=,"Price":)(\d+)', response.text).group(1)
        if street := re.search(r'({"street":{"id":"\d*","code":"","name":")(.+?)(?=")', response.text):
            street = street.group(2)
        room_count = re.search(r'(?<="numberOfRooms":)(\d+)', response.text).group(1)
        price_per_m2 = re.search(r'(?<="key":"price_per_m","value":")(\d+)', response.text).group(1)
        district = re.search(r'(district":{"id":"\d*","code":")(.+?)(?=")', response.text).group(2)
        add_date = re.search(r'(?<=,"createdAt":")(.+?)(?=")', response.text).group(1)

        offer_list.append(Offer(price, street, room_count, price_per_m2, district, add_date))

    except Exception as exc:
        print(exc)
        print("url: ", offer_url)
        print("\n ")


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