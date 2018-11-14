import os
import requests
import re
import csv

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
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                r = requests.post('https://scarlet-labs.appspot.com/optimize', json={'dk_url':chat_text})
                bot.sendMessage(chat_id=chat_id, text=r.text[0:1000])

                text_output = r.text
                buff = csv.StringIO(tmp)
                reader = csv.reader(buff)

                with open("output.csv",'wb') as resultFile:
                    wr = csv.writer(resultFile, dialect='excel')
                    wr.writerows(reader)

                bot.sendDocument(chat_id=chat_id, document=open('output.csv', 'rb'))

            elif chat_text.lower() == "what is my name?":
                say_hello_username = 'Hello {}'.format(update.message.from_user.first_name)
                bot.sendMessage(chat_id=chat_id, text=say_hello_username)

            else:
                bot.sendMessage(chat_id=chat_id, text='try again')
        except:
            return "ok"
