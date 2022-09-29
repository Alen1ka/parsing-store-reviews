from pprint import pprint
import pandas as pd


def parser_google_play(application_name):
    # application_name = edit_app_name(application_name)
    create_excel_file(application_name)
    reviews = [{'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '1'},
               {'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '2'}]
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
    return reviews


def parser_apple(application_name):
    reviews = [{'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '3'},
               {'user_name': 'user_name', 'review': 'review', 'source': 'source', 'date': 'date', 'rating': '4'}]
    '''application_name = edit_app_name(application_name)
    print(application_name)
    # appstore_app = AppStore(country="ru", app_name="sbermegamarket", app_id=946099227)
    appstore_app = AppStore(country="ru", app_name=f"{application_name}")
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
        reviews.append({'user_name': user_name, 'review': review, 'source': source, 'date': date, 'rating': rating})'''
    return reviews


def edit_app_name(application_name):
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                'ю': 'u', 'я': 'ya'}
    return ''.join([alphabet.get(f"{letter}") for letter in application_name.replace(' ', '').lower()])


def create_excel_file(application_name):
    f = f"{application_name}.xlsx"
    df = pd.DataFrame(columns=['user_name', 'review', 'source', 'date', 'rating'])
    df.to_excel(f, index=False)


def writing_to_csv(reviews_app1, reviews_app2, application_name):
    for review_app2 in reviews_app2:
        reviews_app1.append(review_app2)
    #all_reviews_app = [reviews_app1, ]
    f = f"{application_name}.xlsx"
    df = pd.DataFrame(reviews_app1)
    # df.to_excel(f, index=False)
    # xlsx = pd.ExcelFile(f"{application_name}.xlsx")
    # df1 = pd.read_excel(xlsx, "Sheet1")
    # result = pd.concat([df1, df2])
    # print(result)
    df.to_excel(f, index=False)
    # with ExcelWriter(f, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
    #    df.to_excel(writer, sheet_name="Sheet1", index=False, header=None)


if __name__ == '__main__':
    # здесь config
    # print("Введите название приложения и нажмите Enter: ")
    # request = input()
    app_name = edit_app_name('СберМегаМаркет')
    reviews_app_store1 = parser_google_play(app_name)
    reviews_app_store2 = parser_apple(app_name)
    writing_to_csv(reviews_app_store1, reviews_app_store2, app_name)
    # parser_apple(app_name)
