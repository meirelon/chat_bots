import os
import requests
import re
from datetime import datetime
import pandas as pd
import numpy as np


import telegram

def jaccard_dist(a,b):
    a_split = set(list(a.lower()))
    b_split = set(list(b.lower()))
    i = len(a_split.intersection(b_split))
    u = len(a_split.union(b_split))
    return i/u

def get_beer_rec(beer_i_liked):
    beer_df = pd.read_json("https://storage.googleapis.com/beer_recommendations/beer_recommendations.json", lines=True)
    dist_list = [jaccard_dist(beer_i_liked, beer) for beer in beer_df["beer"].unique()]
    beer_match = np.argmax(dist_list)
    question = beer_df["beer"][beer_match]
    answers = [x["rec_beer"] for x in beer_df["recs"][beer_match]]
    return "The recommendations for {beer} are the following: {beer_recommendations}".format(beer=question,
                                                                                            beer_recommendations=", ".join(answers))



def webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True,
                                                          silent=True,
                                                          cache=True), bot)

        try:
            chat_text = update.message.text
            chat_id = update.message.chat.id

            if bool(re.search(string=chat_text.lower(), pattern="draftkings")):
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

            elif bool(re.search(string=chat_text.lower(), pattern="[/]beer")):
                try:
                    beer_name = " ".join(chat_text.split(" ")[1:])
                    beer_recommendation = get_beer_rec(beer_i_liked=beer_name)
                    bot.sendMessage(chat_id=chat_id, text=beer_recommendation)
                except:
                    bot.sendMessage(chat_id=chat_id, text="No Beer Match")

            else:
                bot.sendMessage(chat_id=chat_id, text='try again')
        except:
            return "ok"
