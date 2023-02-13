import os
import telebot
from flask import Flask, request
from auth_data import tg_bot_token, App_URL


bot = telebot.TeleBot(tg_bot_token)
server = Flask(__name__)


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=App_URL)
    return "!", 200


@server.route("/" + tg_bot_token, methods=["POST"])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello " + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))