import os
import requests
import re
from datetime import datetime

from utils import get_beer_rec, get_crypto_price, get_image_emotion
from loginCredentials import oAuth

import telegram


def crypto_webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True,
                                                          silent=True,
                                                          cache=True), bot)

        try:
            chat_text = update.message.text
            chat_id = update.message.chat.id

            #get crypto prices
            if bool(re.search(string=chat_text.lower(), pattern="[/]crypto")):
                try:
                    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                    bot.sendMessage(chat_id=chat_id,
                                    text=get_crypto_price(re.split("\s+", chat_text)[1]))
                except Exception as e:
                    bot.sendMessage(chat_id=chat_id, text=str(e))
            else:
                bot.sendMessage(chat_id=chat_id, text=get_crypto_price("please use crypto function"))

        except Exception as e:
            bot.sendMessage(chat_id=chat_id, text=str(e))


def webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True,
                                                          silent=True,
                                                          cache=True), bot)

        if update.message.photo:
            try:
                chat_id = update.message.chat.id
                fileID = update.message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                photo_link = file_info.file_path

                emotion = get_image_emotion(photo_link=str(photo_link),
                                            image=os.environ["DOCKER_IMAGE"],
                                            instance=os.environ["GCE_INSTANCE"],
                                            zone=os.environ["GCE_ZONE"])

                bot.sendMessage(chat_id=chat_id, text=emotion)
            except Exception as e:
                bot.sendMessage(chat_id=chat_id, text=str(e))



        try:
            chat_text = update.message.text
            chat_id = update.message.chat.id

            if bool(re.search(string=chat_text.lower(), pattern="[/]draftkings")):
                dk_projections_link = "https://storage.googleapis.com/draftkings_lineups/projections_{partition_date}.csv".format(partition_date = datetime.today().strftime("%Y%m%d"))
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                r = requests.post('https://scarlet-labs.appspot.com/optimize', json={'dk_url':chat_text})
                # bot.sendMessage(chat_id=chat_id, text=r.text.split('\n')[1])
                bot.send_message(chat_id=chat_id,
                                 text='<a href="{proj_link}">Click here for link to lineups</a>'.format(proj_link=dk_projections_link),
                                 parse_mode=telegram.ParseMode.HTML)


            elif chat_text.lower() == "what is my name?":
                say_hello_username = 'Hello {}'.format(update.message.from_user.first_name)
                bot.sendMessage(chat_id=chat_id, text=say_hello_username)

            #beer recommendations
            elif bool(re.search(string=chat_text.lower(), pattern="[/]beer")):
                try:
                    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                    beer_name = " ".join(re.split("\s+", chat_text)[1:])
                    beer_recommendation = get_beer_rec(beer_i_liked=beer_name)
                    bot.sendMessage(chat_id=chat_id,
                                    text=beer_recommendation,
                                    parse_mode=telegram.ParseMode.HTML)
                except Exception as e:
                    bot.sendMessage(chat_id=chat_id, text=str(e))

            else:
                bot.sendMessage(chat_id=chat_id, text='try again')
        except:
            return "ok"


def insta_webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True,
                                                          silent=True,
                                                          cache=True), bot)
    try:
        chat_text = update.message.text
        chat_id = update.message.chat.id

        if bool(re.search(string=chat_text.lower(), pattern="[/]login")):
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id, text="Please input your username:")
            if request.method == "POST":
                update = telegram.Update.de_json(request.get_json(force=True,
                                                                  silent=True,
                                                                  cache=True), bot)
                chat_text = update.message.text
                chat_id = update.message.chat.id
                username = chat_test
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text="Please input your password:")

                if request.method == "POST":
                    update = telegram.Update.de_json(request.get_json(force=True,
                                                                      silent=True,
                                                                      cache=True), bot)
                    chat_text = update.message.text
                    chat_id = update.message.chat.id
                    password = chat_text

            login_credentials = oAuth(username=username, password=password)
            u,p,k = login_credentials.encrypt_login()
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id, text="Please try again:")
    except:
        print("Did not work")
