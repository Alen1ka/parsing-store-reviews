import pandas as pd
from pprint import pprint
import numpy as np
import json
# from bs4 import BeautifulSoup
import requests
from google_play_scraper import search
from app_store_scraper import AppStore


def parser(user_request):
    f = f"{user_request}.csv"
    df = pd.DataFrame(columns=['user_name', 'review', 'source', 'date', 'rating'])
    df.to_csv(f, mode='w', index=False)

    # parser_google_play(user_request)
    parser_apple(user_request)

    # dict_reviews = ['Baked', 'Beans', 'shop', '23.03.1222', '2']
    # writing_to_csv(user_request, dict_reviews)


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
    appstore_app = AppStore(country="ru", app_name="yazio-fasting-food-tracker", app_id=946099227)
    appstore_app.review(how_many=20)
    appstore_reviews = appstore_app.reviews
    pprint(appstore_reviews)
    reviews = []
    for review_data in appstore_reviews:
        user_name = review_data['userName']
        review = review_data['review']
        source = 'apple'
        date = review_data['date']
        rating = review_data['rating']
        reviews.append({'user_name': user_name, 'review': review, 'source': source, 'date': date, 'rating': rating})
    # [user_name, review, source, date, rating]
    writing_to_csv(user_request, reviews)
    # df = pd.read_csv(f'{user_request}.csv')
    # df.to_excel(f'{user_request}.xlsx')
    return 0


def writing_to_csv(user_request, dict_reviews):
    f = f"{user_request}.xlsx"
    df = pd.DataFrame(dict_reviews)
    # df = pd.DataFrame({'user_name': [dict_reviews[0]], 'review': [dict_reviews[1]], 'source': [dict_reviews[2]],
    # 'date': [dict_reviews[3]], 'rating': [dict_reviews[4]]})
    # df.to_csv(f, mode='a', index=False, header=False)
    df.to_excel(f)


if __name__ == '__main__':
    # здесь config
    # print("Введите название приложения и нажмите Enter: ")
    # request = input()
    parser('СберМегаМаркет')
