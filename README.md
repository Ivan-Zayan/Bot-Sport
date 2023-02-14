# Description
Telegram bot created to track women's volleyball matches. Its main task is to monitor the score of the match and, under certain conditions, send a notification to the user.
---

The following frameworks were used to implement the bot:
1. requests
2. telebot
3. BeautifulSoup
4. selenium
5. datetime

---

# How to launch a bot
- Downloading the repository
- Creating a virtual environment
- install libraries from a file requirements.txt
- Enter the token of your telegram bot
```
bot = telebot.TeleBot('-------') #Здесь  нужен ТОКЕН Телеграм бота!
```
>The token must be taken from @BotFather in a telegram
- run the file sport_bot22.py
>For the selenium framework to work correctly, you must install the Firefox browser
---

### To see the working commands of the bot, type "/start"
>Attention! The bot will not start working until you manually enter the "запустить отслеживание" command
>Далее код начинает работать и любой пользователь может подключиться к рассылке и отключиться от неё. Отключить отслеживание можно только при помощи остановки исполнения кода.


