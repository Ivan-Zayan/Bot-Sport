import time
from requests import Session
import telebot
from bs4 import BeautifulSoup
from telebot import types
from selenium import webdriver
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36',
    "accept": "*/*",
}
url = 'https://betcity.ru/ru/liveresults/volleyball'
session = Session()
taks = session.get('https://betcity.ru/ru/liveresults/volleyball', headers=headers)
soup = BeautifulSoup(taks.text, 'lxml')
prob = soup.find('div', class_='live-results-champ')
uzer_spisok = []
spisok = []
on_off = 1
spisok_game = {}
last_spisok = []

bot = telebot.TeleBot('-------') #Здесь  нужен ТОКЕН Телеграм бота!


def get_with_selenium(url):
    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override',
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36")
    try:
        driver = webdriver.Firefox(
            executable_path="\ivanz\OneDrive\Рабочий стол\второй лвл\geckodriver",
            options=options
        )
        driver.get(url=url)
        time.sleep(7)

        with open('driver_proba.html', 'w', encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    with open('driver_proba.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    try:
        proba = soup.find('div', class_='live-results-wrapper ps')
        prob = proba.find_all('div', class_='live-results-champ')
    except:
        proba = soup.find('div', class_='live-results-wrapper ps ps--active-y')
        prob = proba.find_all('div', class_='live-results-champ')
    for i in prob:
        match = i.text
        if 'Волейбол' in match:
            if 'Женщины' in match:
                score = i.find_all('div', class_='live-results-event')
                for i in score:
                    score_0 = i.find('span', class_='live-results-event__score-additional').text
                    name = i.find('span', class_='live-results-event__name').text
                    score_1 = score_0.replace(' ', '').replace('(', '').replace(')', '').replace(':', ',')
                    score_2 = list(map(int, score_1.split(',')))
                    spisok_game[name] = score_2
                    spisok.append(score_2)
    return spisok


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'приветствую тебя <b>{message.from_user.first_name} {message.from_user.last_name}</b>, ты можешь узнать счёт, кликнув на кнопошку. ' \
           f'Также, можешь включить уведомления, ыыы'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    real_time = types.KeyboardButton('Присылать вернячки')
    off_button = types.KeyboardButton('Отключить вернячки')
    markup.add(real_time, off_button)
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'кнопошка', reply_markup=markup)


@bot.message_handler()
def set_user(message):
    global on_off
    if message.text == 'Отключить вернячки':
        if message.chat.id in uzer_spisok:
            uzer_spisok.remove(message.chat.id)
            bot.send_message(message.chat.id, 'вернячки отключены', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'вы не включали вернячки', parse_mode='html')

    if message.text == 'Присылать вернячки':
        if message.chat.id in uzer_spisok:
            bot.send_message(message.chat.id, 'вы уже включили вернячки', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'вернячки включены', parse_mode='html')
            uzer_spisok.append(message.chat.id)
            print(uzer_spisok)

    if message.text == 'запустить отслеживание' and on_off == 1:
        on_off += 1
        while True:
            get_with_selenium('https://betcity.ru/ru/liveresults/volleyball')
            for i in spisok:
                if len(i) > 3:
                    if i[0] + i[1] > 46 and i[2] + i[3] > 46 and len(uzer_spisok) != 0:
                        for key, zn in spisok_game.items():
                            if key not in last_spisok and zn == i:
                                last_spisok.append(key)
                                for user in uzer_spisok:
                                    bot.send_message(user, f'скорее делай ставку, это верняк. Играют {key}!',
                                                     parse_mode='html')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(current_time)
            time.sleep(150)


bot.polling(none_stop=True)
