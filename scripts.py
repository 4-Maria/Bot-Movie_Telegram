import requests
from bs4 import BeautifulSoup
import pandas as pd

# Ссылка
def foo(web=0):  # день в который нужно собрать инфу, 0 - сегодня, 1 - завтра
    if web == 0:
        url = 'https://www.kinosfera-imax.ru/#/'
    else:
        if web == 1:
            url = 'https://www.kinosfera-imax.ru/tomorrow'
        else:
            print("День не найден.")

    website = requests.get(url).text
    soup = BeautifulSoup(website, 'lxml')

    dic_films = []

    name = soup.find_all('div', {'class': 'card__title'})  # Название фильма
    href = soup.find_all('div', {'class': 'card__title'})  # ссылка на страницу фильма

    href = soup.find_all('div', {'class': 'card__title'})
    url = []
    for u in range(len(href)):
        url.append(href[u].a.get('href'))

    for i in range(len(name)):
        d = [(name[i].find('span').text), url[i]]

        dic_films.append(d)
        dictionary = dict(dic_films)
    return dictionary

# Постер
def bar(web=0):  # день в который нужно собрать инфу, 0 - сегодня, 1 - завтра
    if web == 0:
        url = 'https://www.kinosfera-imax.ru/#/'
    else:
        if web == 1:
            url = 'https://www.kinosfera-imax.ru/tomorrow'
        else:
            print("День не найден.")

    website = requests.get(url).text
    soup_pic = BeautifulSoup(website, 'lxml')

    dic_pos = []

    pic = soup_pic.find_all('div', {'class': 'card__poster-image cursor-pointer'})  # Постер
    poster = []
    for pos in range(len(pic)):
        poster.append(pic[pos].get('style').replace("background-image: url('", '').replace("')", ""))

    name = soup_pic.find_all('div', {'class': 'card__title'})  # Название фильма
    for i in range(len(name)):
        w = [(name[i].find('span').text), poster[i]]

        dic_pos.append(w)
        image = dict(dic_pos)
    return image


# Главный парсер
def day(web=0):  # день в который нужно собрать инфу, 0 - сегодня, 1 - завтра
    if web == 0:
        url = 'https://www.kinosfera-imax.ru/#/'
    else:
        if web == 1:
            url = 'https://www.kinosfera-imax.ru/tomorrow'
        else:
            print("День не найден.")

    website = requests.get(url).text
    soup = BeautifulSoup(website, 'lxml')

    card_num = soup.find_all('div', {'class': 'card'})  # карточки с фильмами

    lst_time = []  # ВРЕМЯ сеансов (список)
    for v in range(len(card_num)):
        t = card_num[v].find_all('div', {'class': 'time-card__time'})  # нахожу все карточки с временем
        time = []  # сюда собираю все сеансы по каждому фильму отдельно
        for tm in range(len(t)):  # кол-во найденных элем-ов с тэгом 'time-card__time'
            time.append(
                t[tm].text.replace('\xa0', ""))  # убираю все лишнее из строки, оставляю только время в виде "11:15"
            while ("" in time):  # удаляю пустые строки из списка
                time.remove("")
        lst_time.append(time)  # полученный список из сеансов по одному фильму добавляю в общий список "lst"

    dic_films = []  # Хранилище для словаря "d" {Название, Постер, время + стоимость, ссылка на страницу}

    lst_price = []  # СТОИМОСТЬ (список)
    for x in range(len(card_num)):
        p = card_num[x].find_all('div', {'class': 'time-card__price'})
        price = []
        for pr in range(len(p)):
            price.append(p[pr].text.replace('\n', "").replace('от', "").strip() + " ₽")
        lst_price.append(price)

    comm = []  # объединяю время и стоимость
    for q in range(len(lst_time)):
        comm.append([x + ' Цена: ' + y for x, y in zip(lst_time[q], lst_price[q])])

    pic = soup.find_all('div', {'class': 'card__poster-image cursor-pointer'})  # Постер
    poster = []
    for pos in range(len(pic)):
        poster.append(pic[pos].get('style').replace("background-image: url('", '').replace("')",""))
        # убираю лишнее - ["background-image: url('] и [')]

    name = soup.find_all('div', {'class': 'card__title'})  # Название фильма

    href = soup.find_all('div', {'class': 'card__title'})  # ссылка на страницу фильма
    page = []
    for u in range(len(href)):
        page.append(href[u].a.get('href'))

    for i in range(len(name)):  # Собираю словарь
        d = {'Фильм': (name[i].find('span').text),
             'Постер': poster[i],
             'Время и стоимость': comm[i],
             'url': page[i]}
        dic_films.append(d)

    df = pd.DataFrame(dic_films)
    return df