import json
import locale
import sqlite3
from datetime import datetime


def create_table(connection):
    cur = connection.cursor()

    create_car = '''
    CREATE TABLE IF NOT EXISTS "car" (
        "ID"         INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Car"        TEXT NOT NULL,
        "brandID"    INTEGER,
        "type_of_car"TEXT NOT NULL,
        "seating"    TEXT NOT NULL,
        "city"       TEXT NOT NULL,
        "highway"    TEXT NOT NULL,
        "drivetrain" TEXT NOT NULL,
        "horsepower" TEXT NOT NULL,
        "overallrating"  FLOAT,
        "safety"     FLOAT,
        "Performance"FLOAT,
        "interior"   FLOAT,
        "MSRP"       TEXT NOT NULL,
        FOREIGN KEY (brandID) REFERENCES brand(brandID)
        );
    '''


    create_brand = '''
    CREATE TABLE IF NOT EXISTS "brand" (
        "brandID"         INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Brand"      TEXT NOT NULL
        );
    '''
    cur.execute(create_car)
    cur.execute(create_brand)
    connection.commit()


def insert_data(data, conn):
    for i, key in enumerate(data.keys()):
        print(key, i)
        d = data[key]
        cur = conn.cursor()

        insert_car = '''
        INSERT INTO car
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        # extract elements
        name = d['name']
        type_of_car = d['type_of_car']
        seating = d['seating']
        brand = d['brand']
        city = d['city']
        highway = d['highway']
        drivetrain = d['drivetrain']
        horsepower = d['horsepower']
        try:
            overallrating = float(d['overallrating'])
        except:
            overallrating = 0.0
        try:
            safety = float(d['safety'][:3])
        except:
            safety = 0.0
        performance = float(d['performance'][:3])
        
        interior = float(d['interior'][:3])
        print(interior)
        MSRP = d['MSRP']
        car_list_ = [name, brand, type_of_car, seating, 
                    city, highway, drivetrain, horsepower, 
                    overallrating, safety, performance, interior, MSRP]
        
        cur.execute(insert_car, car_list_)
        conn.commit()

#         name = d['name']
#         country = d['country']
#         star = float(d['star'])
#         language = d['language']
#         genre = d['genre']
#         try:
#             dt = datetime.strptime(d['date'], '%d %B %Y')
#         except:
#             d['date'] = "15 " + d['date']
#             dt = datetime.strptime(d['date'], '%d %B %Y')
#         budget = money_exchange(d['box']['budget'])
#         us = money_exchange(d['box']['usa'])
#         world = money_exchange(d['box']['world'])

#         movie_ls = [name, i+1, genre, country, star,
#                     language, dt, budget, us, world]

#         cur.execute(insert_movies, movie_ls)
#         conn.commit()

#         for director in d['directors']:
#             insert_director = '''
#             INSERT INTO director
#             VALUES (NULL, ?, ?)
#             '''
#             director_ls = [director, i+1]
#             cur.execute(insert_director, director_ls)
#             conn.commit()

#         for writer in d['writers']:
#             insert_writer = '''
#             INSERT INTO writer
#             VALUES (NULL, ?, ?)
#             '''
#             writer_ls = [writer, i+1]
#             cur.execute(insert_writer, writer_ls)
#             conn.commit()


        brand = d['brand']
        print(brand)
        insert_brand = '''
        INSERT INTO brand
        VALUES (NULL,?)
        '''
        brand_ls = [brand]
        cur.execute(insert_brand, brand_ls)
        conn.commit()


if __name__ == "__main__":
    connection = sqlite3.connect("car.sqlite")
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    create_table(connection)


    with open('cache/car_info_cache.json') as f:
        data = json.load(f)
    insert_data(data, connection)