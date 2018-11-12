import os
import telegram

def webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        say_hello_username = 'Hello {}'.format(update.message.from_user.first_name)
        # Reply with the same message
        bot.sendMessage(chat_id=chat_id, text=update.message.text)
        # bot.sendMessage(chat_id=chat_id, text=say_hello_username)
    return "ok"
