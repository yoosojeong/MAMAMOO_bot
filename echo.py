# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
   This is built on the API wrappe.
   As a MAMAMOO fan, I wanted to talk to MAMAMOO.
   Then I added the features I needed.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import random
import requests
from bs4 import BeautifulSoup

update_id = None
start = True

def start(bot):
    """Start message"""

    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

    name = None


    update.message.reply_text("무무 이름이 뭐야?")

    if update.message.text != "/start":
        if name is None:
         name = update.message.text
         update.message.reply_text(f"{name}무무~ 반가워 \n실시간 멜론 차트 순위를 보고싶다면 'melon'\n나와 미니게임을 하고싶다면 'game' 를 입력해줘!")

         return name

def echo(bot, name):
    """Echo the message the user sent."""

    global update_id
    # Request updates after the last update_id

    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            if(update.message.text == "melon"):
                melon(bot, update, name)

            if(update.message.text == "game"):
                game(bot, update, name)


def melon(bot,update,name):
    """Send a message when the command /start is issued."""
    update.message.reply_text("현재 마마무의 멜론차트 순위누~ 오늘도 숨스열스~")
    req = requests.get('https://www.melon.com/chart/index.htm')
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    my_titles = soup.select(
        'span > a'
    )

    i = 0

    for title in my_titles:
        if title.text == "마마무":
            update.message.reply_text(f"{title.text} - {my_titles[i-1].text} 순위 : {i//2}위")
        i = i + 1
    echo(bot,name)
def game(bot,update,name):
    """Send a message when the command /start is issued."""
    update.message.reply_text("휘인봇과 함께하는 숫자~야구")
    sleep(1)
    update.message.reply_text("나는 3개의 숫자를 마음 속으로 생각했어!")
    sleep(1)
    update.message.reply_text(f"{name}무무에게 4번의 기회를 줄테니 그 숫자를 맞춰줘~")
    sleep(1)
    update.message.reply_text(f"맞을 땐 스트라이크! 다른 땐 볼!")
    sleep(3)
    update.message.reply_text("시작하누!")
    computer = []
    strike = 0
    ball = 0

    for i in range(1,4):
        computer.append(random.randrange(1,10))
        computer = list(set(computer))
        if len(computer) != 4:
            continue
    update.message.reply_text(f"휘인봇이 생각한 숫자 {computer}")

    while(True):
        if (strike < 4 and ball < 4):
            update.message.reply_text(f"{name}무무가 생각한 숫자는??")

            user = random.randrange(1,10)
            update.message.reply_text(user)

            if user != "game":
                if update.message:
                    update.message.reply_text(user)
                    user = int(user)

                    if user in computer:
                        strike += 1
                        update.message.reply_text(f"{strike}번 스트라이크")
                        continue

                    else:
                        ball += 1
                        update.message.reply_text(f"{ball}번 볼")
                        continue
        break
    if strike == 4:
        update.message.reply_text(f"{name}무무의 승이누~")
    elif ball == 4:
        update.message.reply_text(f"나의 승이누~~")

    echo(bot, name)
def exit(bot,update,error):
    pass
def main():
    """Run the bot."""
    global update_id
    global start
    # Telegram Bot Authorization Token
    bot = telegram.Bot('513900136:AAEjp75FyUUrsOozRBaX1zr7TaIxAI_yG-8')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.

    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if(update.message.text == "/start"):
        update.message.reply_text("안녕 무무 어서와! 나는 마마무 채팅 봇이야~")

        start(bot)
        name = start(bot)

        if name is not None:
            while True:
                try:
                    echo(bot, name)
                except NetworkError:
                    sleep(1)
                except Unauthorized:
                    # The user has removed or blocked the bot.
                    update_id += 1

if __name__ == '__main__':
    main()