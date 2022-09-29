import pandas as pd
from google_play_scraper import app, Sort, reviews
from app_store_scraper import AppStore
from pprint import pprint
# from app_store_scraper import Podcast
# from itunes_app_scraper.scraper import AppStoreScraper
import numpy as np
import json
from bs4 import BeautifulSoup
import requests


def parser(user_request):
    f = f"{user_request}.csv"
    df = pd.DataFrame(columns=['user_name', 'review', 'source', 'date', 'rating'])
    df.to_csv(f, mode='w', index=False)

    parser_google_play(user_request)
    parser_apple(user_request)

    # dict_reviews = ['Baked', 'Beans', 'shop', '23.03.1222', '2']
    # writing_to_csv(user_request, dict_reviews)


def parser_google_play(user_request):
    result = app(
        'com.nianticlabs.pokemongo',
        lang='en',  # defaults to 'en'
        country='us'  # defaults to 'us'
    )
    print(result)
    return 0


def parser_apple(user_request):
    tiktok = AppStore(country="us", app_name="tiktok")
    tiktok.review(how_many=15)
    print(tiktok.reviews)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone &_sacat=0&LH_TitleDesc=0&Model=Apple%20iPhone%208&_sop=12&LH_PrefLoc=0&rt=nc&Storage%20Capacity=64%20GB&_dcat=9355'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    df = pd.DataFrame(np.array(tiktok.reviews), columns=['review'])
    df2 = df.join(pd.DataFrame(df.pop('review').tolist()))
    df2.head()
    df2.to_csv('/Users/Desktop/App Store Review tiktok.csv')
    return 0


def writing_to_csv(user_request, dict_reviews):
    f = f"{user_request}.csv"
    df = pd.DataFrame({'user_name': [dict_reviews[0]], 'review': [dict_reviews[1]], 'source': [dict_reviews[2]],
                       'date': [dict_reviews[3]], 'rating': [dict_reviews[4]]})
    df.to_csv(f, mode='a', index=False, header=False)


if __name__ == '__main__':
    # здесь config
    # print("Введите название приложения и нажмите Enter: ")
    # request = input()
    parser('СберМегаМаркет')
