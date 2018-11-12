import os
import telegram

def webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True,
                                                          silent=True,
                                                          cache=True), bot)

        if update is None:
            return "not ok"
        try:
            chat_id = update.message.chat.id
            if update.message.text.lower() == "what is my name?":
                say_hello_username = 'Hello {}'.format(update.message.from_user.first_name)
                bot.sendMessage(chat_id=chat_id, text=say_hello_username)
            else:
                bot.sendMessage(chat_id=chat_id, text=update.message.text)
            return "ok"
