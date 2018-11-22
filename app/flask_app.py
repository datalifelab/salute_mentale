#!/home/user/venv/bin python

import os
import os.path


import json
import datetime

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from collections import OrderedDict

from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    linux = True
elif _platform == "darwin":
    linux = True
elif _platform == "win32":
    linux = False

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def base():
    return("server work!")

@app.route("/id/<cellulare>")
def index(cellulare):
    datetime.datetime.now()
    with open("./domande_users/" + str(cellulare) + ".json") as questionario: #dati non è un nome appropriato
        dati = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(questionario.read())

    with open("DB_domande.json") as DB_domande:
        DB_domande_dict = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(DB_domande.read())
    print(DB_domande_dict)
    
    with open("./risposte_ex_ante/" + cellulare, "r") as ex_ante:
        ex_ante_dict = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(ex_ante.read())

    prossima_somministrazione = [] # il nome prossima_somministrazione è improprio... qui si intende fino a quando dura la seguente sessione del questionario
    '''
    try:
    '''
    for somministrazione in dati.keys():
        # print(datetime.datetime.strptime(somministrazione, "%y-%m-%d %H"))
        if datetime.datetime.strptime(somministrazione, "%y-%m-%d %H") > datetime.datetime.now():
            prossima_somministrazione.append(somministrazione)

    somministrazione_attuale = prossima_somministrazione[0]
    print(somministrazione_attuale)

    domande_somministrate = []


    #attenzione, perché il sistema funzioni nel questionario devono essere presenti almeno una data di somministrazione in più a quella attuale!
    for item in dati[somministrazione_attuale]:
        print(item)
        domande_somministrate.append(DB_domande_dict[str(item)])

    print(cellulare + "_" + somministrazione_attuale)    

    if os.path.exists("./risposte_users/" + str(cellulare) + "_" + str(somministrazione_attuale)) == True:
        return "hai già risposto, compila il questionario successiovo alla prossima notifica"
    else:
        return render_template("index2.html", cellulare = cellulare, dati = domande_somministrate, orario = somministrazione_attuale , ex_ante = ex_ante_dict)

@app.route("/risultato", methods=['POST'])
def risultato():
    result = request.form
    with open("./risposte_users/" + result["cellulare"] + "_" + result["orario"], "w") as risposta:
        risposta.write(json.dumps(result, ensure_ascii=False, indent=4))


    return("<p> grazie della risposta </p> + <b>{}".format(json.dumps(result, ensure_ascii=False, indent=4)))


@app.route("/ex_ante/<id>")
def ex_ante(id):
    
    with open("./domande_ex_ante/domande_ex_ante.json") as questionario: #dati non è un nome appropriato
        dati = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(questionario.read())

    with open("DB_domande.json") as DB_domande:
        DB_domande_dict = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(DB_domande.read())
    print(DB_domande_dict)
    
    domande_somministrate = []
    for item in dati["ex_ante"]:
        print(item)
        domande_somministrate.append(DB_domande_dict[str(item)])

        
    print(id + "_" + "ex_ante")
    
    

    if os.path.exists("./risposte_ex_ante/" + str(id)) == True:
        with open("./risposte_ex_ante/" + str(id), "r") as risposta:
            risposte = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(risposta.read())
        
        
        
        
        return render_template("ex_ante.html", cellulare = id, dati = domande_somministrate, orario = "ex_ante", presente = "si", risposte = risposte)
    else:
        return render_template("ex_ante.html", cellulare = id, dati = domande_somministrate, presente = "no", orario = "ex_ante")
    
    

@app.route("/risultato_ex_ante", methods=['POST'])
def risultato_ex_ante():
    result = request.form
    with open("./risposte_ex_ante/" + result["cellulare"], "w") as risposta:
        risposta.write(json.dumps(result, ensure_ascii=False, indent=4))


    return("<p> grazie della risposta </p> + <b>{}".format(json.dumps(result, ensure_ascii=False, indent=4)))    
    




if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5050, debug=True,  ssl_context=("../certificate/server2.crt", "../certificate/server2.key"))
