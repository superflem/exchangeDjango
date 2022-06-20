from curses import has_key
from urllib import response
from rest_framework.decorators import api_view
import json # già installato
from django.http import  HttpResponse, FileResponse
import jwt
from db.views import Query # importo le query al db
import os

query = Query()

def controlla_corpo(request):
    body = {}

    try: # controllo che il body sia stato scritto in modo corretto
        body = request.body.decode('utf-8')
        body = json.loads(body)
    except:
        return False
    return body


# endpoint per la signup
@api_view(['OPTION', 'POST'])
def signup(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")
    
    body = controlla_corpo(request) # controllo sia un json
    if (body == False):
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    # controllo gli attributi
    if (not ("nome" in body and "cognome" in body and "iban" in body and "password" in body and "email" in body)): # controllo che ci siano tutti gli attributi
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    return HttpResponse(json.dumps(query.signup(body)))

# endpoint per il login
@api_view(['OPTION', 'POST'])
def login(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    body = controlla_corpo(request) # controllo sia un json
    if (body == False):
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    # controllo gli attributi
    if (not ("password" in body and "email" in body)): # controllo che ci siano tutti gli attributi
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    [rispostaDb, id] = query.login(body)
    response = HttpResponse(json.dumps(rispostaDb)) # effettuo il login
    if (id):
        token = jwt.encode(id, "password") # crea il jwt
        response.set_cookie('jwt', token, max_age=900, httponly='true') # setta il cookie jwt che dura per massimo 15 minuti in modo httponly

    return response


# endpoint per la query dei soldi
@api_view(['OPTION', 'POST'])
def queryy(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token

        [euro, dollari, nome] = query.query(decodificato["id"])
        return HttpResponse(json.dumps({"ridirezione": False, "isTuttoOk":True, "euro": euro, "dollari": dollari, "nome": nome}))
    except Exception as e:
        return HttpResponse(json.dumps({"ridirezione": True, "isTuttoOk":False}))


# endpoint per il logout
@api_view(['OPTION', 'POST'])
def logout(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    response = HttpResponse("logout")
    response.set_cookie('jwt', "", max_age=1, httponly='true') # tolgo il cookie
    return response

# endpoint per le richieste al db che richiedono valuta e valore
@api_view(['OPTION', 'POST'])
def deposit_withdraw_buy(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    body = controlla_corpo(request) # controllo sia un json
    if (body == False):
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    # controllo gli attributi
    if ((not ("valuta" in body and "valore" in body)) or float(body["valore"]) <= 0 or (not(body["valuta"] == "EUR") and not(body["valuta"] == "USD"))): # controllo che ci siano tutti gli attributi
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token

        risposta = {}
        # in base alla richiesta, eseguo una determinata funzione
        if (request.path == "/buy/"): 
            risposta = query.buy(decodificato["id"], body["valuta"], body["valore"])
        elif (request.path == "/deposit/"):
            risposta = query.deposit(decodificato["id"], body["valuta"], body["valore"])
        else:
            risposta = query.withdraw(decodificato["id"], body["valuta"], body["valore"])

        return HttpResponse(json.dumps(risposta))
    except Exception as e:
        return HttpResponse(json.dumps({"ridirezione": True, "isTuttoOk":False}))

# endpoint per le richieste al db che richiedono valuta e valore
@api_view(['OPTION', 'POST'])
def listTransactions(request):
    
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    body = controlla_corpo(request) # controllo sia un json
    if (body == False):
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    # controllo gli attributi
    if (not ("data" in body and "valuta" in body)): # controllo che ci siano tutti gli attributi
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))
    
    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token
        

        risposta = query.listTransactions(decodificato["id"], body["valuta"], body["data"])

        return HttpResponse(json.dumps(risposta))
    except Exception as e:
        return HttpResponse(json.dumps({"ridirezione": True, "isTuttoOk":False}))





#from db.serializers import UtenteSerializer
# endpoint per le richieste al db che richiedono valuta e valore
@api_view(['OPTION', 'POST'])
def uploadImage(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    try:
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token

        risposta = query.updateImage(decodificato["id"], request.FILES["foto"])

        return HttpResponse(json.dumps(risposta))

    except Exception as e:
        print("aaa: ", e)
        return HttpResponse(json.dumps({"isTuttoOk": False, "ridirezione": True}))



# from db.serializers import UtenteSerializer
# endpoint per restituire la foto
@api_view(['OPTION', 'POST'])
def getImage(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    #return HttpResponse(json.dumps({"messaggio": "ciao"}))

    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token
        

        risposta = query.getImage(decodificato["id"])

        return FileResponse(risposta)
    except Exception as e:
        return HttpResponse(json.dumps({"ridirezione": True, "isTuttoOk":False}))



    
    