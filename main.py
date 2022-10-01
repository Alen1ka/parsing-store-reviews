import pandas as pd
from google_play_scraper import search, Sort, reviews
from app_store_scraper import AppStore
import json
from loguru import logger as log

log.add('.\\log\\parser shop {time:DD-MM-YYYY}.log', format='{time:HH:mm:ss.SSSZ} | [{level}]\t| {message}',
        level='ERROR')


def parser_reviews_google_play(application_name):
    try:
        # получение кода приложения
        code = search_app_google_play(application_name)
        # получение отзывов с google play
        result, continuation_token = reviews(
            code,
            lang=LANG,
            country=COUNTRY,
            sort=Sort.NEWEST,  # вывести самые новые отзывы
            count=REVIEWS_COUNT
        )
        # получение для каждого отзыва необходимых характеристик
        google_reviews = []
        for google_review in result:
            google_reviews = create_a_dict_of_reviews(google_reviews, google_review['userName'],
                                                      google_review['content'], 'google', google_review['at'],
                                                      google_review['score'])
        print("Отзывы с google получены.")
        return google_reviews
    except Exception as e:
        log.error(e)


def search_app_google_play(application_name):
    try:
        result = search(
            application_name,
            lang=LANG,
            country=COUNTRY,
            n_hits=1  # вывести только одно название приложения
        )
        code = result[0]['appId']
        return code
    except Exception as e:
        log.error(e)


def parser_reviews_apple(application_name):
    # перевод названия на русский язык
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                'ю': 'u', 'я': 'ya'}
    application_name = ''.join([letter if alphabet.get(f"{letter}") is None else alphabet.get(f"{letter}") for letter in
                                application_name.lower().replace(' ', '-')])
    try:
        # получение отзывов с apple
        appstore_app = AppStore(country=COUNTRY, app_name=f"{application_name.lower().replace(' ', '-')}")
        appstore_app.review(how_many=REVIEWS_COUNT)
        appstore_reviews = appstore_app.reviews
        # получение для каждого отзыва необходимых характеристик
        apple_reviews = []
        for review_data in appstore_reviews:
            apple_reviews = create_a_dict_of_reviews(apple_reviews, review_data['userName'], review_data['review'],
                                                     'apple', review_data['date'], review_data['rating'])
        print("Отзывы с apple получены.")
        return apple_reviews
    except Exception as e:
        log.error(e)


def create_a_dict_of_reviews(shop_reviews, user_name, review, source, date, rating):
    # получение даты в нужном формате
    date = f'{date.day}-{date.month}-{date.year}'
    # формирование словаря с отзывами
    shop_reviews.append(
        {'user_name': user_name, 'review': review, 'source': source, 'date': date, 'rating': rating})
    return shop_reviews


def write_to_excel(reviews_app1, reviews_app2, application_name):
    # соединение словарей магазинов в один
    if reviews_app2 is not None:
        for review_app in reviews_app2:
            reviews_app1.append(review_app)
    # запись в эксель файл
    file_name = f"{application_name}.xlsx"
    df = pd.DataFrame(reviews_app1, columns=['user_name', 'review', 'source', 'date', 'rating'])
    df.to_excel(file_name, index=False)


if __name__ == '__main__':
    # чтение переменных из файла и запись в глобальные переменные
    with open('conf.json', 'r', encoding='utf-8') as f:
        text = json.load(f)

    APP_NAME = text['app_name']
    REVIEWS_COUNT = text['reviews_count']
    COUNTRY = text['country']
    LANG = text['lang']

    reviews_app_store = parser_reviews_google_play(APP_NAME)
    reviews_google_play = parser_reviews_apple(APP_NAME)

    write_to_excel(reviews_app_store, reviews_google_play, APP_NAME)
