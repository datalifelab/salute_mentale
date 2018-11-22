import sys
sys.path.insert(0, '../')
from config import TOKEN, HOST, PORT, CERT, CERT_KEY

token=TOKEN

#nel crontab va messo tutto il path /home/scarselli/anaconda3/bin/python
# e cron.py deve essere eseguibile

import telegram
import time
import sys
from time import gmtime, strftime
import os
from dateutil.tz import tzlocal
from datetime import datetime


def send_message(orario):
    bot = telegram.Bot(token=token)
    IDs = os.listdir("/home/user/DDL-CRF/app/domande_users")

    for identificativi in IDs:
        if identificativi[0] != ".":
            ids = int(identificativi[:-5])
            bot.sendMessage(int(ids), "{} è il momento di compilare il questionario https://survey.eu:5000/id/{} delle ore {}".format(orario, ids,  datetime.now(tzlocal())))


send_message(sys.argv[1])
