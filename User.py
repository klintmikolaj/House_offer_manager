import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg') # For opening pyplots in new windows
import numpy as np
import mysql.connector
from matplotlib.ticker import FuncFormatter

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
        print(MAGENTA + "> appd " + WHITE + "- displays the chart of average price per district " + RESET)
        print(MAGENTA + "> arcpd " + WHITE + "- displays the chart of average room count per district " + RESET)
        print(MAGENTA + "> amppd " + WHITE + "- displays the chart of average m2 price per district" + RESET)
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
            command = input(WHITE + "Give me some instructions > " + RESET)
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
        self.db_cursor.execute("SELECT district, AVG(price) as average_price FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()
        district_prices = {row[0]: self.float_to_int(row[1]) for row in results}

        # Sortowanie dzielnic od największej do najmniejszej średniej ceny
        sorted_district_prices = sorted(district_prices.items(), key=lambda item: item[1], reverse=True)
        districts, average_prices = zip(*sorted_district_prices)  # Rozpakowanie do oddzielnych list
        y_pos = np.arange(len(districts))

        plt.figure(figsize=(10, 8))
        bars = plt.barh(y_pos, average_prices, color='#2990cc')
        plt.yticks(y_pos, districts)

        plt.gca().invert_yaxis()
        plt.gca().xaxis.set_major_formatter(FuncFormatter(self.millions_formatter))

        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():,}',
                     va='center', ha='left', fontsize=6)
        plt.title('Średnia cena mieszkań na dzielnicę')
        plt.xlabel('Średnia cena')
        plt.ylabel('Dzielnica')
        plt.tight_layout()
        plt.grid(color='grey', linestyle='-', linewidth=0.25)
        plt.show()


    def average_room_count_per_district(self):
        self.db_cursor.execute("SELECT district, AVG(room_count) as average_room_count FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()
        district_room_counts = {row[0]: row[1] for row in results}

        # Sortowanie dzielnic od największej do najmniejszej średniej liczby pokoi
        sorted_district_room_counts = sorted(district_room_counts.items(), key=lambda item: item[1], reverse=True)

        districts, average_room_counts = zip(*sorted_district_room_counts)  # Rozpakowanie do oddzielnych list
        y_pos = np.arange(len(districts))

        plt.figure(figsize=(8, 8))
        bars = plt.barh(y_pos, average_room_counts, color='#ebdb02')
        plt.yticks(y_pos, districts)
        plt.gca().invert_yaxis()

        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.1f}',
                     va='center', ha='left', fontsize=8)
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

        # Sortowanie dzielnic od największej do najmniejszej średniej liczby pokoi
        sorted_district_room_counts = sorted(district_price_per_m2.items(), key=lambda item: item[1], reverse=True)

        districts, average_room_counts = zip(*sorted_district_room_counts)  # Rozpakowanie do oddzielnych list
        y_pos = np.arange(len(districts))

        plt.figure(figsize=(10, 8))  # Ustawienie sensownych rozmiarów wykresu
        bars = plt.barh(y_pos, average_room_counts, color='#eb021d')
        plt.yticks(y_pos, districts)

        plt.gca().invert_yaxis()
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.1f}',
                     va='center', ha='left', fontsize=6)
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
                     va='center', ha='left', fontsize=9)

        plt.tight_layout()
        plt.grid(color='grey', linestyle='-', linewidth=0.25)
        plt.show()


test = User()
test.user()


