import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from celery import Celery

app = Celery('tasks')


@app.task
def save_func(article_list):
    """
    Функция для сохранения ссылок в json файл.
    """

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f'articles-{timestamp}.json'
    print('Создание и запись в файл.')

    with open(filename, 'w') as file:
        json.dump(article_list, file)


@app.task
def get_rss(arg):
    """
    Ф-ция сканирует и парсит страницу сохраняя в лист ссылки и
    заголовки статей.
    """

    article_list = []

    try:
        response = requests.get(arg)
        print('Доступ к ресурсу: код -> ', response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', class_='storylink')

        for a in articles:
            link = a.get('href')
            title = a.get_text()

            article = {
                'created': str(datetime.now()),
                'title': title,
                'link': link,
            }
            article_list.append(article)

        return save_func(article_list)

    except Exception as e:
        print('Скрапинг не удался.')
        print('Ошибка: ', e)


if __name__ == '__main__':
    url = 'https://news.ycombinator.com'
    print('Запуск процесса.')

    # celery задача
    from celery.schedules import crontab
    app.conf.beat_schedule = {
        # выполняеться каждую минуту
        'scraping-task-one-min': {
            'task': 'main.get_rss',
            'schedule': crontab(),
        }
    }

    get_rss(url)
    print('Завершение.')
