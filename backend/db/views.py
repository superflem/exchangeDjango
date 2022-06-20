# from django.shortcuts import render

# Create your views here.

from db.models import Utente, Transizione
import requests # pip install requests
import xmltodict # pip install xmltodict
from datetime import datetime # funzione che restituisce la data attuale
import json
import os

#funzione che effetua il cambio euro dollaro prendendo 
# l'attale cambio in tempo reale dal file xml della bce
def cambio(valuta, valore):
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml?46f0dd7988932599cb1bcac79a10a16a"
    response = requests.get(url) # contatto il link e trasformo il file xml in un dizionario
    data = xmltodict.parse(response.content)

    cambio = 1
    for valute in data["gesmes:Envelope"]["Cube"]["Cube"]["Cube"]: #cerco i dollari
        if (valute["@currency"] == "USD"):
            cambio = valute["@rate"]
            break
    
    if (valuta == "EUR"): # calcolo il valore
        return float(valore) * float(cambio)
    else:
        return float(valore) / float(cambio)



class Query():
    def signup(self, body):
        try: # controllo che email e iban non siano già in uso
            utente = Utente(nome=body["nome"], cognome=body["cognome"], email=body["email"], password=body["password"], iban=body["iban"], euro=0, dollari=0, foto="default.png")
            utente.save()
            return {"isTuttoOk": True, "messaggio": "Utente inserito correttamente"}
        except Exception as e:
            response = {"isTuttoOk": False}
            if ("email" in str(e)): # analizzo gli errori
                response["messaggio"] = "Email già in uso"
            elif ("iban" in str(e)):
                response["messaggio"] = "IBAN già in uso"
            else:
                response["messaggio"] = "Errore inatteso"
            return response

    def login(self, body):
        risultati = Utente.objects.filter(email=body["email"], password=body["password"]) # faccio il login, se l'utente non esiste restituisco false
        if (len(list(risultati)) == 0):
            return [{"isTuttoOk": False, "messaggio": "Email o password non corretti"}, False]
        else:
            return [{"isTuttoOk": True, "messaggio": "Autenticazione avvenuta"}, {"nome":risultati[0].nome, "id": risultati[0].id}] # altrimenti restituisco id e nome

    def query(self, id): # query per trovare quanti soldi ha un utente
        risultati = Utente.objects.get(id=id)
        return [risultati.euro, risultati.dollari, risultati.nome]

    def withdraw(self, id, valuta, valore): # deposita i soldi dalla piattaforma al cc.
        risultati = Utente.objects.get(id=id)
        if (valuta == "USD"): # guardo se euro o dallari
            if (risultati.dollari < float(valore)): #controllo di avere abbastanza soldi
                return {"isTuttoOk": False, "ridirezione": False, "errore": "non hai abbastanza soldi"}
            else:
                risultati.dollari = risultati.dollari - float(valore)
                risultati.save()
                return {"isTuttoOk": True, "ridirezione": False, "messaggio": "Deposito avvenuto con successo"}
        else:
            if (risultati.euro < float(valore)):
                return {"isTuttoOk": False, "ridirezione": False, "errore": "non hai abbastanza soldi"}
            else:
                risultati.euro = risultati.euro - float(valore)
                risultati.save()
                return {"isTuttoOk": True, "ridirezione": False, "messaggio": "Deposito avvenuto con successo"}

    def deposit(self, id, valuta, valore): # faccio il prelievo dal cc al conto corrente
        risultati = Utente.objects.get(id=id)
        if (valuta == "USD"):
            risultati.dollari = risultati.dollari + float(valore)
        else:
            risultati.euro = risultati.euro + float(valore)
        
        risultati.save()
        return {"isTuttoOk": True, "ridirezione": False, "messaggio": "Conto caricato con successo"}

    def buy(self, id, valuta, valore): # cambio valuta
        risultati = Utente.objects.get(id=id)
        if (valuta == "USD"): # controllo se voglio cambiare euro o dallari
            valuta_comp = "EUR"
            if (risultati.dollari < float(valore)): # controllo di avere abbastanza soldi
                return {"isTuttoOk": False, "ridirezione": False, "errore": "non hai abbastanza soldi"}
            else:
                risultati.dollari = risultati.dollari - float(valore) #faccio il cambio
                comprato = float(cambio(valuta, valore))
                risultati.euro = risultati.euro + comprato
                risultati.save()
                #inserisco la nuoa transizione nel db
                transizione = Transizione(fk_utente=risultati, quantita_spesa=valore, quantita_comprata=comprato, valuta_comprata=valuta_comp, data=datetime.today())
                transizione.save()
                return {"isTuttoOk": True, "ridirezione": False, "messaggio": "Cambio avvenuto con successo"}
        else:
            valuta_comp = "USD"
            if (risultati.euro < float(valore)):
                return {"isTuttoOk": False, "ridirezione": False, "errore": "non hai abbastanza soldi"}
            else:
                risultati.euro = risultati.euro - float(valore)
                comprato = float(cambio(valuta, valore))
                risultati.dollari = risultati.dollari + comprato
                risultati.save()
                transizione = Transizione(fk_utente=risultati, quantita_spesa=valore, quantita_comprata=comprato, valuta_comprata=valuta_comp, data=datetime.today())
                transizione.save()
                return {"isTuttoOk": True, "ridirezione": False, "messaggio": "Cambio avvenuto con successo"}

    def listTransactions(self, id, valuta, data):
        # imposto la query
        if (not(valuta == "") and not(data == "")):
            tabella = Transizione.objects.filter(fk_utente=id, valuta_comprata=valuta, data=data)
        elif (not(valuta == "")):
            tabella = Transizione.objects.filter(fk_utente=id, valuta_comprata=valuta)
        elif (not(data == "")):
            tabella = Transizione.objects.filter(fk_utente=id, data=data)
        else:
            tabella = Transizione.objects.filter(fk_utente=id)

        # inserisco i risultati nel dizionario
        risultati = {"ridirezione": False, "isTuttoOk": True, "listaTransizioni": []}
        for i in tabella:
            nuovo = {}
            nuovo["data"] = str(i.data)
            nuovo["valuta_comprata"] = i.valuta_comprata
            nuovo["quantita_spesa"] = i.quantita_spesa
            nuovo["quantita_comprata"] = i.quantita_comprata
            risultati["listaTransizioni"].append(nuovo)
            
        return risultati


    def updateImage(self, id, file):
        try:
            risultati = Utente.objects.get(id=id) # trovo l'utente
            # rinomino il file con l'hash dell'id e lo salvo nel db
            id_hashato = hash(str(id))
            nome_file = str(id_hashato) + ".png"
            risultati.foto = nome_file
            risultati.save()

            #salvo il file
            with open('foto/'+nome_file, 'wb+') as destinazione:
                for chunk in file.chunks():
                    destinazione.write(chunk)
            
            return {"isTuttoOk": True, "ridirezione": False, "messaggio": "Immagine del profilo aggiornata con successo"}
        except Exception as e:
            return {"isTuttoOk": False, "ridirezione": False, "messaggio": "Qualcosa è andato storto"}

        

    def getImage(self, id): 
        risultati = Utente.objects.get(id=id)
        
        percorso = risultati.foto
        print(percorso)

        percorso = os.path.abspath('') + "/foto/" + percorso
        print(percorso)
        img = open(percorso, 'rb')
        return img
