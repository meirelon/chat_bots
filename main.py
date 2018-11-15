import os
import requests
import re
from datetime import datetime

import telegram



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
                                 text='<a href="{proj_link}">Click here for link to lineups</a>.'.format(proj_link=dk_projections_link),
                                 parse_mode=telegram.ParseMode.HTML)


            elif chat_text.lower() == "what is my name?":
                say_hello_username = 'Hello {}'.format(update.message.from_user.first_name)
                bot.sendMessage(chat_id=chat_id, text=say_hello_username)

            else:
                bot.sendMessage(chat_id=chat_id, text='try again')
        except:
            return "ok"
