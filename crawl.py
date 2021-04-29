from bs4 import BeautifulSoup
import requests
import json
import os.path
from datetime import datetime
CAR_CACHE_FILENAME = "cache/car_cache.json"
CAR_INFO_CACHE_FILENAME = "cache/car_info_cache.json"
CAR_URL_DICT = {}
CAR_INFO_DICT = {}
class Car:
    def __init__(self, name, brand, type_of_car, seating, city, highway, 
                drivetrain, horsepower, overallrating, safety, performance,
                interior, MSRP):
        self.name = name or ""
        self.brand = brand or ""
        self.type_of_car = type_of_car or ""
        self.seating = seating or ""
        self.city = city or ""
        self.highway = highway or ""
        self.drivetrain = drivetrain or ""
        self.horsepower = horsepower or ""
        self.overallrating = overallrating or ""
        self.safety = safety or ""
        self.performance = performance or ""
        self.interior = interior or ""
        self.MSRP = MSRP or ""
    def info(self):
        s = self.name
        return s


def get_car_url_dict():
    ''' Make a dictionary that maps cars name to state page url from "https://cars.usnews.com/cars-trucks/rankings/compact-suvs"
    Parameters
    ----------
    None
    Returns
    -------
    dict
        key is a car name and value is the url
        e.g. {'2021 Honda CR-V':'https://cars.usnews.com/cars-trucks/honda/cr-v', ...}
    '''

    global CAR_URL_DICT

    # Check if file exists
    if not CAR_URL_DICT:
        # Requires and download html from website
        print ("Fetching cars")
        car_name_dict = {}
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://cars.usnews.com/cars-trucks/rankings/compact-suvs/"
        r = requests.get(url, headers = headers, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser') ## .text
        
        # Using Find and place items in dictionary
        cars = soup.find(id = "full-rankings")
        all_cars_list = cars.find_all(class_="DetailCardAutosRankings__Container-gyznnz-0 fBqWty mb5")

        # Construct the dictionary of {'cx-5':'https://cars.usnews.com/cars-trucks/mazda/cx-5'}
        for item in all_cars_list:
            if item.find('a').contents[0].get('aria-label') is None:
                key = item.find('a').contents[0].find('img').get('alt')
            else:
                key = item.find('a').contents[0].get('aria-label')
            
            val = item.find(class_ = 'mt0 mb2 lg-mb3').find('a').get('href')
            print(item.find(class_ = 'mt0 mb2 lg-mb3').find('a').get('href'))
            print("------------------------------------------")
            car_name_dict[key] = "https://cars.usnews.com" + val
        CAR_URL_DICT = car_name_dict
        save_cache(CAR_URL_DICT, CAR_CACHE_FILENAME)
        return CAR_URL_DICT

    else:
        print ("Using cache")
        return CAR_URL_DICT


def get_cars_instance(car):
    '''Make an instances from a car URL.
    
    Parameters
    ----------
    car:
        The car name
    
    Returns
    -------
    instance
        a car instance
    '''
    if car in CAR_INFO_DICT.keys():
        print("Using cache")
        return CAR_INFO_DICT[car]
    else:
        print("Fetching Car Info!")
        car_url = CAR_URL_DICT[car]
        headers = {'User-Agent': 'Mozilla/5.0'}
        r_craw = requests.get(car_url, headers = headers, allow_redirects=True)
        soup_craw = BeautifulSoup(r_craw.text, "html.parser")

        # Get name
        name = car.split()[2]
        # Get brand
        brand = car.split()[1]
        # Get type
        try:
            type_of_car = soup_craw.find(class_ = "hero-title__subheader hero-title__subheader--overview").find('a').text
        except:
            temp = soup_craw.find(class_ = "rankings-widget-box").find('h2').text
            type_of_car = temp.split()[1] + " " + temp.split()[2]
            print(type_of_car)
        # Get seating
        seating = soup_craw.find(id = "seatingInfo").find('strong').text
        # Get city and highway
        city = soup_craw.find(class_ = "mpg specs-bar__info").find_all('strong')[0].text
        highway = soup_craw.find(class_ = "mpg specs-bar__info").find_all('strong')[1].text
        # Get drivetrain
        drivetrain = soup_craw.find(id = "drivetrainInfo").find('strong').text
        # Get Horsepower
        horsepower = soup_craw.find(id = "hp").find('strong').text
        # Get overallrating
        overallrating = soup_craw.find(class_ = "scorecard__score").text
        # safety
        safety = soup_craw.find(class_ = "scorecard-list scorecard__list").find(class_ = "display-block").find_all(class_ = "display-block clearfix block-tighter")[3].find_all('td')[1].text.strip()
        # performance
        performance = soup_craw.find(class_ = "scorecard-list scorecard__list").find(class_ = "display-block").find_all(class_ = "display-block clearfix block-tighter")[1].find_all('td')[1].text.strip()
        # interior
        interior = soup_craw.find(class_ = "scorecard-list scorecard__list").find(class_ = "display-block").find_all(class_ = "display-block clearfix block-tighter")[2].find_all('td')[1].text.strip()
        # MSRP
        try:
            MSRP = soup_craw.find(class_ = "bpp-widget__msrp").find(class_ = "bold line-through").text
        except:
            MSRP = None

        car_object = Car(name, brand, type_of_car, seating, city, highway, 
                drivetrain, horsepower, overallrating, safety, performance,
                interior, MSRP)
        CAR_INFO_DICT[car] = car_object.__dict__
        # save_cache(CAR_INFO_DICT, "cache/car_info_cache" + "_" + str(name) + ".json")
        save_cache(CAR_INFO_DICT, CAR_INFO_CACHE_FILENAME)
        
        return CAR_INFO_DICT

def open_cache(cache_filename):
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(cache_filename, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, filename):
    ''' Saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''

    dumped_json_cache = json.dumps(
        cache_dict, default=lambda o: o.__dict__, indent=4)
    fw = open(filename, "w")
    fw.write(dumped_json_cache)
    fw.close()

if __name__ == "__main__":
    if not os.path.exists('cache_data'):
        os.makedirs('cache_data')
    CAR_URL_DICT = open_cache(CAR_CACHE_FILENAME)
    CAR_INFO_DICT = open_cache(CAR_INFO_CACHE_FILENAME)

    car_name_dict = get_car_url_dict()
    for i, key in enumerate(CAR_URL_DICT.keys()):
        print(i, key)
        get_cars_instance(key)
