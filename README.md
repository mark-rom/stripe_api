# stripe_api
____

### Описание: ###
Тестовое задание для [Ранкс](https://ranks.pro/)

Из предложенных заданий выполнено:
- создана модель Item с полями name, description, price;
- создан API с двумя методами: `GET /buy/{id}` и `GET /item/{id}`;
- для хранения ключа stripe-api использованы переменные окружения;
- модель Item зарегистрирована в панели Django Admin;
- решение залито на Github, запуск описан в Readme.md.


Метод `GET /item/{id}` возвращает получить простейшую HTML страницу с информацией о выбранном Item и кнопкой Buy.

По нажатию на кнопку Buy происходит запрос к эндпойнту `/buy/{id}`.

Метод `GET /buy/{id}` создает Checkout Session с помощью библиотеки stripe и возвращает session.id, который впоследствии обрабатывается с помощью JS библиотеки Stripe. Происходит редирект на Checkout форму.

После заполнения формы пользователю возвращается HTML страница с сообщением о прошедшем платеже. В случае отказа от заполнения формы пользователю возвращается страница отмены платежа.
____

## Установка: ##

### Клонируйте репозиторий: ###
    git clone git@github.com:mark-rom/stripe_api.git

### Перейдите в репозиторий в командной строке: ###
    cd stripe_api
  
### Создайте и активируйте виртуальное окружение: ###
    python3.9 -m venv venv

###### для Mac OS
    source venv/bin/activate

###### для Windows OS
    source venv/Scripts/activate
  
### Установите зависимости из файла requirements.txt: ###
### Обновите pip:
    python3 -m pip install --upgrade pip

### Установите зависимости:
    pip install -r requirements.txt

### Предоставьте переменные окружения: ###
Для работы API необходимо вручную создать .env файл с переменными окружения:
- stripe_key (Пример: sk_test_4eC39HqLyjWDarjtT1zdp7dc)
- django_secret_key (Пример: *_uep#-69ry%vf+hk_=%+*da&5!!csv64hi9wui+t$ft9=w!*e)

Обратите внимание, что stripe предоставляет два API key, в переменную окружения нужно внести `Secret key`.

### Выполните миграции: ###
    python3 manage.py migrate

### Заполните базу данных из csv файла: ###
    python3 manage.py populate_item item.csv

### Создайте суперюзера: ###
    python3 manage.py createsuperuser

### Запустите проект: ###
    python3 manage.py runserver