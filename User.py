from matplotlib import pyplot as plt
import mysql.connector

class User:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="root", passwd="eloelo320", database="homes")
        self.db_cursor = self.db.cursor()

    def connect_to_db(self):
        self.db_cursor.execute("USE homes")
        self.db.commit()

    def create_plot(self):
        self.connect_to_db()
        self.db_cursor.execute("SELECT price FROM homes_tb;")
        price = self.db_cursor.fetchall()
        self.db_cursor.close()
        tab = [price[0] for price in price]
        print(tab)
        tab_val = [i for i in range(1, len(tab) + 1)]
        print(tab_val)
        plt.plot(tab, tab_val)
        plt.show()




test = User()
test.create_plot()
