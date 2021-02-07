import requests
from bs4 import BeautifulSoup


def get_rss(arg):
    article_list = []
    try:
        response = requests.get(arg)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', class_='storylink')

        for a in articles:
            link = a.get('href')
            title = a.get_text()

            article = {
                'title': title,
                'link': link,
            }
            article_list.append(article)

        return save_func(article_list)

    except Exception as e:
        print('Скрапинг не удался.')
        print('Ошибка: ', e)


def save_func(article_list):
    with open('hacker_news.txt', 'w') as file:
        for a in article_list:
            file.write(str(a)+'\n')
        file.close()


url = 'https://news.ycombinator.com'

if __name__ == '__main__':
    print('Начало...')
    get_rss(url)
    print('Конец.')
