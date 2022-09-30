import urllib
from pprint import pprint
from urllib.request import urlopen

import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import ssl
from google_play_scraper import Sort, reviews

from app_store_scraper import AppStore
import urllib.error
from serpapi import GoogleSearch

# import requests
# import os
# import warnings
# from tqdm import tqdm
# from selenium.webdriver.common.keys import Keys

'''def download_permitted(address):
    f = urlopen("http://" + address + "/config?action=get&paramid=eParamID_MediaState")'''


def parser_google_play(application_name):
    z = 1
    while z == 1:
        try:

            result, continuation_token = reviews(
                'com.fantome.penguinisle',
                lang='en',  # defaults to 'en'
                country='us',  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.NEWEST
                count=3,  # defaults to 100
                filter_score_with=5  # defaults to None(means all score)
            )
            print(continuation_token)
            print(result)

            # If you pass `continuation_token` as an argument to the reviews function at this point,
            # it will crawl the items after 3 review items.

            result, _ = reviews(
                'com.fantome.penguinisle',
                continuation_token=continuation_token  # defaults to None(load from the beginning)
            )
            print(result)
            print(_)

            '''app_reviews = reviews_all(
                app_id='43243',
                sleep_milliseconds=0,
                country='us',
                count=200
            )
            print(app_reviews)'''
            z = 0
        except ConnectionError as e:
            z = 1
            # print(e)
        except urllib.error.URLError as e:
            z = 1
            # print(e)
        except Exception as e:
            z = 1
            print(e)
    '''
    # print(requests.get(
    #    f'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{application_name}/reviews'))

    '''
    '''reviews_list = []
    ratings_list = []

    # Windowless mode feature (Chrome) and error message handling.
    options = webdriver.ChromeOptions()
    options.headless = True  # Runs driver without opening a chrome browser.
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # Initialization of web driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://play.google.com/store/games')

    reviews = driver.find_elements(by=By.CLASS_NAME, value="h3YV2d")  # Locates reviews
    star_ratings = driver.find_elements(by=By.CLASS_NAME, value="iXRFPc")  # Locates ratings
    # time.sleep(WAIT_TIME)
    for (review, rating) in zip(reviews, star_ratings):
        review = review.text  # Extracts reviews
        star_rating = rating.get_attribute("aria-label")  # Extracts the strings from "aria-label" attribute
        star_rating = re.findall("\d", star_rating)  # Extracts the integer rating as list
        star_rating = star_rating[0]  # Removes rating from list

        reviews_list.append(review)  # adds each review to reviews list
        ratings_list.append(star_rating)  # adds each rating to ratings list

    # Creates dictionary and adds list of reviews and ratings
    # app_reviews_ratings["reviews"] = reviews_list
    # app_reviews_ratings["ratings"] = ratings_list
    driver.quit()  # Closes driver window and ends driver session'''
    # context = ssl._create_unverified_context()
    # urllib.urlopen("https://no-valid-cert", context=context)

    # ssl._create_default_https_context = ssl._create_unverified_context
    '''result = search(
        "best Pikachu game",
        lang="en",  # defaults to 'en'
        country="us",  # defaults to 'us'
        n_hits=3  # defaults to 30 (= Google's maximum)
    )
    print(result)
    lang = "jp"
    country = "jp"
    id = "jp.go.mhlw.covid19radar"'''

    google_reviews = [{'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '1'},
                      {'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '2'}]
    return google_reviews


def parser_apple(application_name):
    apple_reviews = [{'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '3'},
                     {'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '4'}]
    application_name = edit_app_name(application_name)
    print(application_name)
    # appstore_app = AppStore(country="ru", app_name="sbermegamarket", app_id=946099227)
    appstore_app = AppStore(country="ru", app_name=f"{application_name}")
    appstore_app.review(how_many=20)
    appstore_reviews = appstore_app.reviews
    pprint(appstore_reviews)
    apple_reviews = []
    for review_data in appstore_reviews:
        user_name = review_data['userName']
        review = review_data['review']
        source = 'apple'
        dt = review_data['date']
        date = f'{dt.day}-{dt.month}-{dt.year}'
        rating = review_data['rating']
        apple_reviews.append(
            {'user_name': user_name, 'review': review, 'source': source, 'date': date, 'rating': rating})
    return apple_reviews


def edit_app_name(application_name):
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                'ю': 'u', 'я': 'ya'}
    return ''.join([alphabet.get(f"{letter}") for letter in application_name.replace(' ', '').lower()])


def writing_to_csv(reviews_app1, reviews_app2, application_name):
    f = f"{application_name}.xlsx"

    for review_app2 in reviews_app2:
        reviews_app1.append(review_app2)

    df = pd.DataFrame(reviews_app1, columns=['user_name', 'review', 'source', 'date', 'rating'])
    df.to_excel(f, index=False)


if __name__ == '__main__':
    # здесь config
    # print("Введите название приложения и нажмите Enter: ")
    # request = input()
    app_name = edit_app_name('СберМегаМаркет')
    reviews_app_store1 = parser_google_play(app_name)
    reviews_app_store2 = parser_apple(app_name)
    writing_to_csv(reviews_app_store1, reviews_app_store2, app_name)
