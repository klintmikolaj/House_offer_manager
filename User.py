from matplotlib import pyplot as plt
import numpy as np
import mysql.connector
from matplotlib.ticker import FuncFormatter

class User:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="root", passwd="eloelo320", database="homes")
        self.db_cursor = self.db.cursor()

    def float_to_int(self, x):
        if float(x) == int(x):
            return int(x)
        else:
            return float(x)

    @staticmethod
    def millions_formatter(x, pos):
        return f'{int(x)}'

    @staticmethod
    def room_formatter(x, pos):
        """Formatuje liczby pokoi z maksymalnie jednym miejscem dziesiętnym."""
        return f'{x:.1f}'

    def create_plot(self):
        self.db_cursor.execute("SELECT price FROM homes_tb;")
        price = self.db_cursor.fetchall()
        self.db_cursor.close()
        tab = [price[0] for price in price]
        print(tab)
        tab_val = [i for i in range(1, len(tab) + 1)]
        print(tab_val)
        plt.plot(tab, tab_val)
        plt.show()

    def average_price_per_district(self):
        self.db_cursor.execute("SELECT district, AVG(price) as average_price FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()
        district_prices = {row[0]: self.float_to_int(row[1]) for row in results}

        # Sortowanie dzielnic od największej do najmniejszej średniej ceny
        sorted_district_prices = sorted(district_prices.items(), key=lambda item: item[1], reverse=True)

        districts, average_prices = zip(*sorted_district_prices)  # Rozpakowanie do oddzielnych list
        y_pos = np.arange(len(districts))

        plt.figure(figsize=(10, 8))  # Ustawienie sensownych rozmiarów wykresu
        bars = plt.barh(y_pos, average_prices, color='#969696')
        plt.yticks(y_pos, districts)

        # Odwrócenie osi Y, aby najwyższe wartości były na górze
        plt.gca().invert_yaxis()
        plt.gca().xaxis.set_major_formatter(FuncFormatter(self.millions_formatter))

        # Dodanie etykiet wartości przy każdym słupku
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():,}',
                     va='center', ha='left')

        # Dodanie tytułu i etykiet osi
        plt.title('Średnia cena mieszkań na dzielnicę')
        plt.xlabel('Średnia cena')
        plt.ylabel('Dzielnica')
        plt.show()


    def average_room_count_per_district(self):
        self.db_cursor.execute("SELECT district, AVG(room_count) as average_room_count FROM homes_tb GROUP BY district")
        results = self.db_cursor.fetchall()
        district_room_counts = {row[0]: row[1] for row in
                                results}  # Założenie, że AVG(room_count) zwraca wartość zmiennoprzecinkową

        # Sortowanie dzielnic od największej do najmniejszej średniej liczby pokoi
        sorted_district_room_counts = sorted(district_room_counts.items(), key=lambda item: item[1], reverse=True)

        districts, average_room_counts = zip(*sorted_district_room_counts)  # Rozpakowanie do oddzielnych list
        y_pos = np.arange(len(districts))

        plt.figure(figsize=(10, 8))  # Ustawienie sensownych rozmiarów wykresu
        bars = plt.barh(y_pos, average_room_counts, color='#969696')
        plt.yticks(y_pos, districts)

        plt.gca().invert_yaxis()
        plt.gca().xaxis.set_major_formatter(FuncFormatter(self.room_formatter))

        # Dodanie etykiet wartości przy każdym słupku
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.1f}',
                     va='center', ha='left')

        # Dodanie tytułu i etykiet osi
        plt.title('Średnia liczba pokoi na dzielnicę')
        plt.xlabel('Średnia liczba pokoi')
        plt.ylabel('Dzielnica')
        plt.show()

    def average_room_price_per_district(self):
        ...



test = User()
test.average_room_count_per_district()
