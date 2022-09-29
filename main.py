import pandas as pd
from pprint import pprint
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
    return 0


def parser_apple(user_request):
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
