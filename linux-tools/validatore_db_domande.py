import pandas as pd
import json


# qui si analizza se il DB_domande è importabile in json
with open("DB_domande.json") as json_file:
   try:
      data = json.loads(json_file.read())
   except Exception as e:
      print("formattazione errata all'interno della stringa:\
       {}".format(e))
      print("correggere!")
      exit()

# qui si intende controllare se le "celle" del db domande sono le formato corretto
pandas_checker = pd.DataFrame(data)
controllo_tipo_domanda = pandas_checker.applymap(type).apply(pd.value_counts, axis=1)
controllo_tipo_domanda.columns = controllo_tipo_domanda.columns.to_series().apply(str)

DOMANDA = ("DOMANDA", controllo_tipo_domanda.loc["DOMANDA", "<class 'str'>"] == controllo_tipo_domanda.loc["DOMANDA"].sum())
MOD_RISPOSTA = ("MOD_RISPOSTA",  controllo_tipo_domanda.loc["MOD_RISPOSTA", "<class 'list'>"] == controllo_tipo_domanda.loc["MOD_RISPOSTA"].sum())
ORARIO  = ("ORARIO",  controllo_tipo_domanda.loc["ORARIO", "<class 'list'>"] == controllo_tipo_domanda.loc["ORARIO"].sum())
TYPE = ("TYPE", controllo_tipo_domanda.loc["TYPE", "<class 'str'>"] == controllo_tipo_domanda.loc["TYPE"].sum())

print("effettua un controlli in {}".format("DB-domande.xlsx"))
pd.DataFrame(data).T.to_excel("DB-domande.xlsx")