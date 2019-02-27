import os
import requests
import re
from datetime import datetime
import telegram

#all foos
from gcloud_utils import upload_blob
from ImageIO import get_image, get_vision_request, get_emotion
from utils import get_beer_rec, get_crypto_price
from loginCredentials import oAuth
from spotipy import get_playlist

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
                get_image(photo_link)
                upload_blob(bucket_name=os.environ["GCS_BUCKET"], source_file_name="/tmp/photo.jpg", destination_blob_name="photo.jpg")

                SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
                SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']

                playlist = get_playlist(clientID=os.environ["SPOTIPY_CLIENT_ID"],
                                        clientSECRET=os.environ['SPOTIPY_CLIENT_SECRET'],
                                        emotion=emotion)

                full_response = "Here is your {emotion} playlist: {playlist}".format(emotion=emotion, playlist=playlist)

                r = get_vision_request(key=os.environ["VISION_API_KEY"], bucket_path=os.environ["GCS_BUCKET"])
                emotion = get_emotion(r)

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
