import json
from datetime import datetime
from pprint import pprint
import requests
import bs4
from fake_headers import Headers


def logger(old_function):
    def new_function(*args, **kwargs):
        call_time = datetime.now()
        function_name = old_function.__name__
        arguments = args, kwargs

        result = old_function(*args, **kwargs)

        with open('task3_main.log', 'a') as f:
            f.write(f"{call_time} - Функция '{function_name}',"
                    f" вызвана с аргументами {arguments},"
                    f" возвращаемое значение {result}\n")

        return result

    return new_function


KEYWORDS = ['дизайн', 'ПК', 'web', 'теория']


def get_fake_headers():
    return Headers(browser='chrome', os='mac').generate()


response = requests.get('https://habr.com/ru/articles/', headers=get_fake_headers())

soup = bs4.BeautifulSoup(response.text, features="lxml")
news_list = soup.findAll('article', class_="tm-articles-list__item")

parsed_data = []


@logger
def find_articles():
    articles = []
    for news in news_list:
        article_info = news.find('a', class_='tm-title__link')
        time_info = news.find('a', class_='tm-article-datetime-published')
        if article_info and time_info:
            title = article_info.find('span').text
            link = article_info['href']
            timestamp = time_info.find('time')["title"]
            for word in KEYWORDS:
                if word in title:
                    print(f'<{timestamp}>-<{title}>-<https://habr.com{link}>')
                    articles.append((title, link, timestamp))
                    break
    return articles


@logger
def dump_json(articles):
    for title, link, timestamp in articles:
        parsed_data.append({
            'title': title,
            'link': link,
            'timestamp': timestamp
        })


articles = find_articles()
dump_json(articles)

with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)

print(f"Записано {len(parsed_data)} статей в articles.json")
