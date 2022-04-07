from tabulate import tabulate
import telebot
import config
import dbworker
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

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["info"])
def cmd_info(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBHrtgaxy1jEDLUuastUuACyyJy3ueKAACbAIAArrAlQUQPz5F8HIrth4E')

    bot.send_message(message.chat.id, "1️⃣ So, what can I do? 🧐\n"
                                      "I can show you the Movie schedule and the price of tickets in Imax.\n"
                                      "First you gotta select the day: \n"
                                      "To get info press /today or /tomorrow. 👀")
    bot.send_message(message.chat.id, "2️⃣ The next step is to select a Movie. 🎬 \n"
                                      "You should select only one ❗️Movie from the list of movies. \n"
                                      "Use the 'Copy-Paste' 🤓 function with the movie list to avoid mistakes. ❌\n"
                                      "You can see the list of the movies 📄 when you select a day.\n"
                                      "You can also type ⌨️the name of the film as it`s given in the list of the movies.\n")
    bot.send_message(message.chat.id, "3️⃣ There's a number of commands you can use here. 👇\n"
                                      "Press /commands to get the list of available functions.\n"
                                      "Press /reset to start anew. 🔁")


@bot.message_handler(commands=["commands"])
def cmd_commands(message):
    bot.send_message(message.chat.id,
                     "/reset - is used to discard previous selections and start anew.\n"
                     "/start - is used to start a new dialogue from the very beginning.\n"
                     "/info - is used to know what I can do for you.\n"
                     "/commands - If you got here, you know what it is used for.\n")
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBHmZgavzpzqTB2Dc17HJHq-0Q2-aGigACdQIAArrAlQUHDPNSndIC4R4E')


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Alright, Bro, let's start anew.\n"
                                      "Which day do you want to get? Press /today or /tomorrow .\n"
                                      "Use /info or /commands to rewind what I am and what can I do.")
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBHrVgaxg2BeIu2p2Q-fmS8AI_yV1DxQACcAIAArrAlQUVFOTJOsDy3h4E')
    dbworker.set_state(message.chat.id, config.States.S_ENTER_DAY.value)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    dbworker.set_state(message.chat.id, config.States.S_START.value)

    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBG19gZ2KtCd7ah_7yevkNoI1Fad7KPwACaQIAArrAlQUw5zOp4KLsaB4E')
    bot.send_message(message.chat.id, "Greetings again, {0.first_name}! \n"
                                      "You gotta specify which day do you want to get, press: /today or /tomorrow.\n"
                                      "Press /info to know what I am and what I can do for you.\n"
                                      "Press /commands to list the available commands.\n"
                                      "Press /reset to discard previous selections and start anew.".format(
                                            message.from_user, bot.get_me()))
                                      # , parse_mode = 'html', reply_markup = markup)

    dbworker.set_state(message.chat.id, config.States.S_ENTER_DAY.value)



@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_DAY.value)
                         and message.text.strip().lower() not in
                         ('/reset', '/info', '/start', '/commands'))
def cmd_day(message):
    dbworker.del_state(str(message.chat.id) + 'day')
    bot.send_message(message.chat.id, "Hold onto the saddle, Bro .... I'm looking for info 🐎💨")
    if message.text.lower().strip() == '/tomorrow':
        # day = 1
        x = day(1)['Фильм']
        bot.send_message(message.chat.id, "\n".join(x))

        bot.send_message(message.chat.id, "Okey-dokey 🤠 you`ve chosen the schedule for tomorrow.\n"
                                          "Now, buddy, choose a movie 🎥 from the list.\n"
                                          "Remember to use 'Copy-Paste' to avoid mistakes.\n"
                                          "Or type film as it`s given in the list of the movies above.\n"
                                          "You could also press /info to know more about me.\n"
                                          "Press /reset to start anew.")
        dbworker.set_property(str(message.chat.id) + 'day', 'tomorrow')  # запишем день в базу
        dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)
    elif message.text.lower().strip() == '/today':
        # day = 0
        x = day()['Фильм']
        bot.send_message(message.chat.id, "\n".join(x))

        bot.send_message(message.chat.id, "Okey-dokey 🤠 you`ve chosen the schedule for today.\n"
                                          "Now, buddy, choose a movie 🎥 from the list.\n"
                                          "Remember to use 'Copy-Paste' to avoid mistakes.\n"
                                          "Or type film as it`s given in the list of the movies above.\n"
                                          "You could also press /info to know more about me.\n"
                                          "Press /reset to start anew.")

        dbworker.set_property(str(message.chat.id) + 'day', 'today')  # запишем день в базу
        dbworker.set_state(message.chat.id, config.States.S_ENTER_FILM.value)
    else:
        bot.send_message(message.chat.id, "Hey, Amigo, seems like you've already got acquainted with me.\n"
                                          "Now's the time to choose a day.\n"
                                          "To get the schedule press: /today or /tomorrow. \n"
                                          "If you need help press /info. 🤏\n"
                                          "Press /reset to start anew.")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBHwABYGsvx6ci09srYUrK_HKJLa-3X68AAn0CAAK6wJUFIEI6nDf-m0YeBA')


@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_FILM.value)
                                          and message.text.strip().lower() not in
                                          ('/reset', '/info', '/start', '/commands'))
# today_answer
def cmd_film(message):
    film = message.text
    df = day()
    bot.send_message(message.chat.id, "All right, Amigo, give me a few seconds 💭")
    if dbworker.get_current_state(str(message.chat.id) + 'day') == 'today':
        y = day()['Фильм']
        lst = list(y)
        df = day()

        errors = []
        if film not in lst:
            errors.append(film)
        else:
            pass

        if errors == []:
            if film != ():
                x = df[['Фильм', 'Время и стоимость']][df['Фильм'] == film].reset_index(drop=True)
                bot.send_photo(message.chat.id, bar(0)[film])
                bot.send_message(message.chat.id, tabulate(x, headers=x.columns, tablefmt="grid"))
                bot.send_message(message.chat.id, "That's it! 😎\n"
                                 "Press on the link and buy 💳 tickets:\n" 
                                 "{www}\n"
                                 "You can choose a another movie or press /reset to start over and change the day."
                                 .format(www=foo(1)[film]))
            else:
                bot.send_message(message.chat.id, 'Something wrong!')
        else:
            bot.send_message(message.chat.id,
                             "Easy-easy, Cherif...🤚🏽"
                             "Something has gone wrong or something that\'s not in our movie list.\n"
                             "Here they are: {here}.\n"
                             "Take a deep breath 🗣...and try again. Use movie list to choose a film.\n"
                             "Or press /reset to start from the beginning.".format(here=", ".join(errors)))
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEBHwNgazNYAAEXm0qTUPcRpj_Fk7wXXOgAAmgCAAK6wJUFluaGRo2p0W0eBA')

# tomorrow_answer
    elif dbworker.get_current_state(str(message.chat.id) + 'day') == 'tomorrow':
        z = day(1)['Фильм']
        lst = list(z)
        df = day(1)

        errors = []
        if film not in lst:
            errors.append(film)
        else:
            pass

        if errors == []:
            if film != ():
                x = df[['Фильм', 'Время и стоимость']][df['Фильм'] == film].reset_index(drop=True)
                bot.send_photo(message.chat.id, bar(1)[film])
                bot.send_message(message.chat.id, tabulate(x, headers=x.columns, tablefmt="grid"))
                bot.send_message(message.chat.id, "That's it! 😎\n"
                                 "Press on the link and buy 💳 tickets:\n"
                                 "{www}\n"
                                 "You can choose a another movie or press /reset to start over and change the day."
                                 .format(www = foo(1)[film]))
            else:
                bot.send_message(message.chat.id, 'Something wrong!')
        else:
            bot.send_message(message.chat.id,
                             "Easy-easy, Cherif...🤚🏽"
                             "Something has gone wrong or something that\'s not in our movie list.\n"
                             "Here they are: {here}.\n"
                             "Take a deep breath 🗣...and try again. Use movie list to choose a film.\n"
                             "Or press /reset to start from the beginning.".format(here=", ".join(errors)))
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEBHwNgazNYAAEXm0qTUPcRpj_Fk7wXXOgAAmgCAAK6wJUFluaGRo2p0W0eBA')
    else:
        pass


if __name__ == '__main__':
     bot.infinity_polling()


