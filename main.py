import os
import requests
import re
import csv

import telegram

def write_list_to_file(guest_list, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in guest_list:
            outfile.write(entries)
            outfile.write("\n")



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
                bot.sendMessage(chat_id=chat_id, text=r.text.split('\n')[1])

                # text_output = r.text.split('\n')
                # write_list_to_file(text_output, 'output.csv')
                # bot.sendDocument(chat_id=chat_id, document=open('output.csv', 'rb'))

            elif chat_text.lower() == "what is my name?":
                say_hello_username = 'Hello {}'.format(update.message.from_user.first_name)
                bot.sendMessage(chat_id=chat_id, text=say_hello_username)

            else:
                bot.sendMessage(chat_id=chat_id, text='try again')
        except:
            return "ok"
