# coding: utf-8

from db.models import Utente

class Signup():
    def signup(self, body):
        # controllo che l'iban abbia il numero di caratteri giusto
        if (not(len(body["iban"]) == 27)):
            return {"isTuttoOk": False, "messaggio": "L'iban non ha il numero di caratteri giusto"}
        
        # controllo che la mail abbia la chiocciola
        if ("@" not in body["email"]):
            return {"isTuttoOk": False, "messaggio": "L'indirizzo email non è valido"}

        # controllo che la password abbia 128 caratteri
        if (not(len(body["password"]) == 128)):
            return {"isTuttoOk": False, "messaggio": "La password non è nel formato corretto"}

        
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