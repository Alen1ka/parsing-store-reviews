import urllib.error
import pandas as pd
from google_play_scraper import Sort, reviews
from google_play_scraper import search
from app_store_scraper import AppStore
import json
from loguru import logger as log

log.add('.\\log\\parser shop {time:DD-MM-YYYY}.log', format='{time:HH:mm:ss.SSSZ} | [{level}]\t| {message}',
        level='ERROR')


def search_google_play(application_name):
    error1 = 1
    while error1 == 1:
        try:
            result = search(
                f"{application_name}",
                lang=LANG,
                country=COUNTRY,
                n_hits=1
            )
            error1 = 0
            code = result[0]['appId']
            return code
        except urllib.error.URLError as e:
            z = 1
        except Exception as e:
            log.error(e)


def parser_google_play(application_name):
    application_name = application_name.lower()
    error2 = 1
    while error2 == 1:
        try:
            code = search_google_play(application_name)
            result, continuation_token = reviews(
                code,
                lang=LANG,
                country=COUNTRY,
                sort=Sort.NEWEST,
                count=COUNT
            )
            error2 = 0
            google_reviews = []
            for google_review in result:
                google_reviews = create_a_dict_of_reviews(google_reviews, google_review['userName'],
                                                          google_review['content'], 'google', google_review['at'],
                                                          google_review['score'])
            return google_reviews
        except urllib.error.URLError as e:
            z = 1
        except Exception as e:
            log.error(e)


def parser_apple(application_name):
    application_name = edit_app_name(application_name)
    z = 1
    while z == 1:
        try:
            appstore_app = AppStore(country=COUNTRY, app_name=f"{application_name.replace(' ', '')}")
            # appstore_app = AppStore(country="ru", app_name="yazio-fasting-food-tracker", app_id=946099227)
            appstore_app.review(how_many=COUNT)
            appstore_reviews = appstore_app.reviews
            apple_reviews = []
            for review_data in appstore_reviews:
                apple_reviews = create_a_dict_of_reviews(apple_reviews, review_data['userName'], review_data['review'],
                                                         'apple',
                                                         review_data['date'], review_data['rating'])

            z = 0
            return apple_reviews
        except AttributeError as e:
            z = 1
        except Exception as e:
            log.error(e)


def create_a_dict_of_reviews(apple_reviews, user_name, review, source, date, rating):
    date = f'{date.day}-{date.month}-{date.year}'
    apple_reviews.append(
        {'user_name': user_name, 'review': review, 'source': source, 'date': date, 'rating': rating})
    return apple_reviews


def edit_app_name(application_name):
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                'ю': 'u', 'я': 'ya'}
    return ''.join([alphabet.get(f"{letter}") for letter in application_name.lower()])


def writing_to_csv(reviews_app1, reviews_app2, application_name):
    f = f"{application_name}.xlsx"

    for review_app2 in reviews_app2:
        reviews_app1.append(review_app2)

    df = pd.DataFrame(reviews_app1, columns=['user_name', 'review', 'source', 'date', 'rating'])
    df.to_excel(f, index=False)


if __name__ == '__main__':
    print("Подождите минут 5, может заработает)")
    with open('conf.json', 'r', encoding='utf-8') as f:
        text = json.load(f)

    APP_NAME = text['app_name']
    COUNT = text['count']
    COUNTRY = text['country']
    LANG = text['lang']

    reviews_app_store1 = parser_google_play(APP_NAME)
    reviews_app_store2 = parser_apple(APP_NAME)
    writing_to_csv(reviews_app_store1, reviews_app_store2, APP_NAME)
