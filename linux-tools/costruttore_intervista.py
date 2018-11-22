import datetime
import json
from collections import OrderedDict
import os.path
 


import sys





#inizio = datetime.datetime(year = 2017, month=12, day =29)


def costruttore_fn(intervistato, inizio, giorni, intervalli):
    """
    intervistato: (str) numero telefonico dell'intervistato
    inizio : (datetime) es. datetime.datetime(year=year, month=month, day=day)
    giorni: (int) numero di giorni proseguirà il questionario
    intervallo: (list) di orari in cui il questionario cambia es [10,14,18,22,24]
    """
    x = 0
    name_file = intervistato
    dict_file = OrderedDict()
    for giorno in range(0,giorni):
        for intervallo in intervalli:
            x = x + 1
            dict_file[(inizio + datetime.timedelta(hours=intervallo)).strftime("%y-%m-%d %H")] = [1,2,3,4,5,6] #mattina
        inizio = inizio + datetime.timedelta(days=1) #aggiunto un giorno


    if not os.path.isfile(intervistato):
        with open("../app/domande_users/" + str(intervistato), "w") as json_file:
            json_file.write(json.dumps(dict_file, indent=2))
    
    
    
        return json.dumps(dict_file, indent=2)
    else:
        print("telephone number just exist!")
        
        
if __name__ == "__main__":     
    numero_telefonico =sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    day = int(sys.argv[4])

    inizio = datetime.datetime(year=year, month=month, day=day)
    intervalli = [10,14,18,22,24]    

    print("per costruire un nuovo diario digitare NUMERO ANNO_INIZIO MESE_INIZIO GIORNO_INIZIO")
    risultato = costruttore_fn(numero_telefonico + ".json", inizio, 100, intervalli)






