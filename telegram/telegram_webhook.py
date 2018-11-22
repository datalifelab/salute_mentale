#!/usr/bin/env python

'''Using Webhook and self-signed certificate'''

from flask import Flask, request

import telegram
import time
import json
import emoji
import sys

sys.path.append("../linux-tools/")

from costruttore_intervista import *
import datetime

import sys
sys.path.insert(0, '../')
from config import TOKEN, HOST, PORT, CERT, CERT_KEY

bot = telegram.Bot(TOKEN)
app = Flask(__name__)
context = (CERT, CERT_KEY)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)
    update_dict = update.to_dict()

    try:
        echo = update_dict["message"]["text"]
        ids = update_dict["message"]["from"]["id"]
        print(echo)
        print(ids)
        #if echo != "meun":
            #bot.sendMessage(chat_id=ids, text='Non ti rispondo perché sono un robot, ma ho capito che hai detto "{}"'.format(echo))
        #else:
        #custom_keyboard = [['top-left', 'top-right'], ['bottom-left', 'bottom-right']]
        if echo == "costruttore_intervista":
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day

            inizio = datetime.datetime(year=year, month=month, day=day)
            intervalli = [10,14,18,22,24]
            risultato = costruttore_fn(str(ids) + ".json", inizio, 100, intervalli)
            bot.send_message(chat_id=ids, text="questionario istanziato per {}".format(ids))
            bot.send_message(chat_id=ids, text="https://survey.datalifelab.eu:5000/id/{}".format(ids))
        elif echo.lower() == "ex_ante":

            bot.send_message(chat_id=ids, text="questionario ex_ante per {}".format(ids))
            bot.send_message(chat_id=ids, text="https://survey.datalifelab.eu:5000/ex_ante/{}".format(ids))


        with open("web_hook.txt", "a") as storage:
            storage.write(str(update))


        print(update)
        return 'OK'
    except:
        return 'ERROR'


def setWebhook():
    bot.setWebhook(url='https://%s:%s/%s' % (HOST, PORT, TOKEN),
                   certificate=open(CERT, 'rb'))

if __name__ == '__main__':
    setWebhook()
    time.sleep(3)

    app.run(host='0.0.0.0',
            port=PORT,
            ssl_context=context,
            debug=True)
