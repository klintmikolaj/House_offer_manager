import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import mysql.connector
from matplotlib.ticker import FuncFormatter
from Core import Core
matplotlib.use('TkAgg') # For opening pyplots in new windows

class User:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="root", passwd="eloelo320", database="homes")
        self.db_cursor = self.db.cursor()

    def help(self):
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
        print(WHITE + "---------------------------------------" + RESET)
        print(BLUE + "This is the help panel" + RESET)
        print(MAGENTA + "> q " + WHITE + "- quits the program" + RESET)
        print(MAGENTA + "> db " + WHITE + "- adds new offers to the database" + RESET)
        print(MAGENTA + "> appd " + WHITE + "- displays the chart of average price per district " + RESET)
        print(MAGENTA + "> arcpd " + WHITE + "- displays the chart of average room count per district " + RESET)
        print(MAGENTA + "> amppd " + WHITE + "- displays the chart of average m2 price per district" + RESET)
        print(MAGENTA + "> od " + WHITE + "- displays the chart showing the offers distribution by district" + RESET)
        print(MAGENTA + "> odp " + WHITE + "- displays the chart showing the offers distribution by district in the pie chart" + RESET)
        print(MAGENTA + "> apbr " + WHITE + "- displays the chart showing the average price for m2 depending on the number of rooms" + RESET)
        print(MAGENTA + "> mes " + WHITE + "- displays the chart of 5 most expensive streets by average price " + RESET)
        print(MAGENTA + "> les " + WHITE + "- displays the chart of 5 least expensive streets by average price " + RESET)
        print(WHITE + "---------------------------------------" + RESET)
    def user(self):
        RED = '\033[91m'
        WHITE = '\033[97m'
        RESET = '\033[0m'

        print(WHITE + "---------------------------------------" + RESET)
        print(RED + "Welcome to the House Offer Manager!" + RESET)
        print(WHITE + "press 'h' to display the help panel" + RESET)
        print(WHITE + "press 'q' to quit" + RESET)
        print(WHITE + "---------------------------------------" + RESET)

        while True:
            command = input(WHITE + "Give me some instructions > " + RESET).strip()
            if command == 'h':
                self.help()
            elif command == 'appd':
                self.average_price_per_district()
            elif command == 'arcpd':
                self.average_room_count_per_district()
            elif command == 'amppd':
                self.average_m2_price_per_district()
            elif command == 'mes':
                self.most_least_expensive_streets('h')
            elif command == 'les':
                self.most_least_expensive_streets('l')
            elif command == "db":
                core_instance = Core()
                core_instance.run()
            elif command == "od":
                self.offer_distribution()
            elif command == "odp":
                self.offer_distribution_pie()
            elif command == "apbr":
                self.avg_price_m2_by_room()
            elif command == "q":
                return 0
            else:
                print(RED + "Unknown instruction, press 'h' to display the help panel" + RESET)
    def float_to_int(self, x):
        if float(x) == int(x):
            return int(x)
        else:
            return float(x)

    @staticmethod
    def millions_formatter(x, pos):
        return f'{int(x)}'

    def average_price_per_district(self):
        # Creates db query
        self.db_cursor.execute("SELECT district, AVG(price) as average_price FROM homes_tb GROUP BY district")

        # Creates the list of tuples where one tuple represents one row in the db
        results = self.db_cursor.fetchall()

        # Creates a dict where a link from an offer is a key value, then sorts it by price
        district_prices = {row[0]: self.float_to_int(row[1]) for row in results}
        sorted_district_prices = sorted(district_prices.items(), key=lambda item: item[1], reverse=True)

        # Unpacks the data to two separate lists
        districts, average_prices = zip(*sorted_district_prices)

        # Sets a proper position for every district name on y-axis
        y_pos = np.arange(len(districts))
        plt.figure(figsize=(12, 8))
        bars = plt.barh(y_pos, average_prices, color='#2990cc')
        plt.yticks(y_pos, districts, size=7)

        plt.gca().invert_yaxis()
        plt.gca().xaxis.set_major_formatter(FuncFormatter(self.millions_formatter))

        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():,}',
                     va='center', ha='left', size=7)

        plt.title('Średnia cena mieszkań na dzielnicę')
        plt.xlabel('Średnia cena')
        plt.ylabel('Dzielnica')
        plt.tight_layout()
        plt.grid(color='grey', linestyle='-', linewidth=0.25)
        plt.show()

    def offer_distribution_pie(self):
        self.db_cursor.execute("SELECT district, COUNT(*) as offers_count FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()

        # Creates a dict from received data
        district_offers = {row[0]: row[1] for row in results}

        total_offers = sum(district_offers.values())
        min_percentage = 0.02  # 2%

        # Process data to group small districts into 'Other'
        small_districts_total = 0
        districts_to_remove = []
        for district, count in district_offers.items():
            if count / total_offers < min_percentage:
                small_districts_total += count
                districts_to_remove.append(district)

        # Remove small districts and add 'Other' category
        for district in districts_to_remove:
            del district_offers[district]
        district_offers['Inne'] = small_districts_total

        # Extracts districts and offers counts
        districts, offers_counts = zip(*district_offers.items())

        plt.figure(figsize=(10, 10))  # Adjust the size as necessary
        plt.pie(offers_counts, labels=districts, autopct='%1.1f%%', startangle=140)
        plt.title('Dystrybucja ofert według dzielnic')

        plt.tight_layout()
        plt.show()

    def offer_distribution(self):
        self.db_cursor.execute("SELECT district, COUNT(*) as offers_count FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()

        # Creates a dict from received data
        district_offers = {row[0]: row[1] for row in results}

        sorted_district_offers = sorted(district_offers.items(), key=lambda item: item[1], reverse=True)

        # Sorting districts from largest to lowest avg room count
        districts, offers_counts = zip(*sorted_district_offers)

        plt.figure(figsize=(20, 8))
        plt.bar(districts, offers_counts, color='skyblue')
        plt.title('Dystrybucja ofert według dzielnic')
        plt.xlabel('Dzielnica')
        plt.ylabel('Liczba ofert')

        # Adds value to certain bars
        for i, count in enumerate(offers_counts):
            plt.text(i, count, f'{count}', ha='center', va='bottom', size=7)

        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.xticks(rotation=90, fontsize=7)
        plt.tight_layout()
        plt.show()

    def average_room_count_per_district(self):
        self.db_cursor.execute("SELECT district, AVG(room_count) as average_room_count FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()
        district_room_counts = {row[0]: row[1] for row in results}

        sorted_district_room_counts = sorted(district_room_counts.items(), key=lambda item: item[1], reverse=True)

        districts, average_room_counts = zip(*sorted_district_room_counts)  # Rozpakowanie do oddzielnych list
        y_pos = np.arange(len(districts))

        plt.figure(figsize=(10, 8))
        bars = plt.barh(y_pos, average_room_counts, color='#ebdb02')
        plt.yticks(y_pos, districts, size=7)
        plt.gca().invert_yaxis()

        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.1f}',
                     va='center', ha='left', size=7)
        plt.title('Średnia liczba pokoi na dzielnicę')
        plt.xlabel('Średnia liczba pokoi')
        plt.ylabel('Dzielnica')
        plt.tight_layout()
        plt.grid(color='grey', linestyle='-', linewidth=0.25)
        plt.show()

    def average_m2_price_per_district(self):
        self.db_cursor.execute("SELECT district, AVG(price_per_m2) as average_room_count FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()
        district_price_per_m2 = {row[0]: row[1] for row in results}

        # Sorting districts from largest to lowest avg room count
        sorted_district_room_counts = sorted(district_price_per_m2.items(), key=lambda item: item[1], reverse=True)

        # Unpacks data to separate lists
        districts, average_room_counts = zip(*sorted_district_room_counts)
        y_pos = np.arange(len(districts))

        plt.figure(figsize=(10, 8))
        bars = plt.barh(y_pos, average_room_counts, color='#eb021d')
        plt.yticks(y_pos, districts, size=7)

        plt.gca().invert_yaxis()

        # Adds data value to every bar
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.1f}',
                     va='center', ha='left', size=7)

        plt.title('Średnia cena m2 na dzielnicę')
        plt.xlabel('Średnia cena m2')
        plt.ylabel('Dzielnica')
        plt.tight_layout()
        plt.grid(color='grey', linestyle='-', linewidth=0.25)
        plt.show()

    def most_least_expensive_streets(self, flag):
        if flag == 'h':
            self.db_cursor.execute(
                "SELECT street, AVG(price_per_m2) as average_price FROM homes_tb GROUP BY street ORDER BY average_price DESC LIMIT 5")
            results = self.db_cursor.fetchall()
        elif flag == 'l':
            self.db_cursor.execute(
                "SELECT street, AVG(price_per_m2) as average_price FROM homes_tb GROUP BY street ORDER BY average_price ASC LIMIT 5")
            results = self.db_cursor.fetchall()

        districts, average_prices = zip(*results)

        plt.figure(figsize=(10, 8))
        bars = plt.barh(districts, average_prices, color='#30db21')
        if flag == 'h':
            plt.title('5 Najdroższych ulic ze średnią ceną za m2')
        elif flag == 'l':
            plt.title('5 Najtańszych ulic ze średnią ceną za m2')
        plt.xlabel('Średnia cena za m2 (PLN)')
        plt.gca().invert_yaxis()

        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():,.0f} PLN',
                     va='center', ha='left')

        plt.tight_layout()
        plt.grid(color='grey', linestyle='-', linewidth=0.25)
        plt.show()

    def avg_price_m2_by_room(self):
        self.db_cursor.execute("""
                SELECT room_count, AVG(price_per_m2) as average_price_per_m2
                FROM homes_tb
                GROUP BY room_count
                ORDER BY room_count
            """)
        results = self.db_cursor.fetchall()
        room_counts, average_prices_per_m2 = zip(*results)


        plt.figure(figsize=(10, 8))
        plt.bar(room_counts, average_prices_per_m2, color='green')
        for i, price in enumerate(average_prices_per_m2):
            plt.annotate(f'{price:.2f}',
                         (room_counts[i], price),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

        plt.title('Średnia cena za metr kwadratowy w zależności od liczby pokoi')
        plt.xlabel('Liczba pokoi')
        plt.ylabel('Średnia cena za m^2 [PLN]')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


