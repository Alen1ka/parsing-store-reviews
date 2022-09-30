import pandas as pd
from google_play_scraper import Sort, reviews
from app_store_scraper import AppStore


def parser_google_play(application_name):
    z = 1
    while z == 1:
        try:
            result, continuation_token = reviews(
                'com.fantome.penguinisle',
                lang='en',  # defaults to 'en'
                country='us',  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.NEWEST
                count=20,  # defaults to 100
                filter_score_with=5  # defaults to None(means all score)
            )
            google_reviews = []
            for google_review in result:
                google_reviews = create_a_dict_of_reviews(google_reviews, google_review['user_name'],
                                                          google_review['content'], 'google', google_review['date'],
                                                          google_review['score'])
                z = 0
            print(google_reviews)
            return google_reviews
        except Exception as e:
            print(e)


def parser_apple(application_name):
    application_name = edit_app_name(application_name)
    appstore_app = AppStore(country="ru", app_name=f"{application_name}")
    appstore_app.review(how_many=20)
    appstore_reviews = appstore_app.reviews
    apple_reviews = []
    for review_data in appstore_reviews:
        apple_reviews = create_a_dict_of_reviews(apple_reviews, review_data['userName'], review_data['review'], 'apple',
                                                 review_data['date'], review_data['rating'])

    return apple_reviews


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
