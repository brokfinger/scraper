# scraper
Скрипт парсящий сайт https://news.ycombinator.com для получения заголовок 
статей и их ссылки в отдельный файл. Использует Celery задачу, чтобы 
самостоятельно каждую минуту чистить файл и добавлять новые записи.

### Стек:
* Python
* requests
* beautifulsoup4
* Celery
* RabbitMQ
* Docker

### Инструкция
1. Скачать исходник.
2. Создать виртуальное окружение: ```python3 -m venv venv```
3. Установить зависимости: ```pip install -r requirements.txt```
4. Запустить файл **main.py**

#### Дополнительно
1. С начала запустить RabbitMQ:
    ```docker run -it --rm --name <name_container> -p 5672:5672 rabbitmq```
2. Потому запустить Celery: ```celery -A main worker -B -l INFO```
