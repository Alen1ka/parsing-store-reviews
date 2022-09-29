import pandas as pd
from pprint import pprint
import datetime
import numpy as np
import json
# from bs4 import BeautifulSoup
import requests
from google_play_scraper import search
from app_store_scraper import AppStore


def parser_google_play(user_request):
    '''result = search(
        "best Pikachu game",
        lang="en",  # defaults to 'en'
        country="us",  # defaults to 'us'
        n_hits=3  # defaults to 30 (= Google's maximum)
    )
    print(result)
    lang = "jp"
    country = "jp"
    id = "jp.go.mhlw.covid19radar"

    app_reviews = reviews_all(
        id,
        sleep_milliseconds=0,
        country=country,
        count=200
    )
    print(app_reviews)'''
    return 0


def parser_apple(user_request):
    # appstore_app = AppStore(country="ru", app_name="sbermegamarket", app_id=946099227)
    appstore_app = AppStore(country="ru", app_name="sbermegamarket")
    appstore_app.review(how_many=20)
    appstore_reviews = appstore_app.reviews
    pprint(appstore_reviews)
    reviews = []
    for review_data in appstore_reviews:
        user_name = review_data['userName']
        review = review_data['review']
        source = 'apple'
        dt = review_data['date']
        date = f'{dt.day}-{dt.month}-{dt.year}'
        rating = review_data['rating']
        reviews.append({'user_name': user_name, 'review': review, 'source': source, 'date': date, 'rating': rating})
    writing_to_csv(user_request, reviews)
    return 0


def writing_to_csv(user_request, dict_reviews):
    f = f"{user_request}.xlsx"
    df = pd.DataFrame(dict_reviews)
    df.to_excel(f)


if __name__ == '__main__':
    # здесь config
    # print("Введите название приложения и нажмите Enter: ")
    # request = input()
    user_request = 'СберМегаМаркет'
    parser_google_play(user_request)
    parser_apple(user_request)
    parser_apple(user_request)
