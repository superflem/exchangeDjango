
from rest_framework.decorators import api_view
import json # già installato
from django.http import  HttpResponse, FileResponse
import jwt
from db.query import Query # importo le query al db
from db.signup import Signup
import requests # pip install requests
import xmltodict # pip install xmltodict
# from backend.controllaCorpo.controlla_corpo as controlla_corpo

# controlla_corpo = controllaCorpo.controlla_corpo

def controlla_corpo(request):
    body = {}
    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        return body
    except:
        return False

query = Query()
signupp = Signup()


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

    return HttpResponse(json.dumps(signupp.signup(body)))

# endpoint per la query dei soldi
@api_view(['OPTION', 'POST'])
def queryy(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token

        [euro, dollari, nome] = query.query(decodificato["id"]["id"])
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

    # controllo gli attributi (che siano dei float)
    try:
        if ((not ("valuta" in body and "valore" in body)) or float(body["valore"]) <= 0 or (not(body["valuta"] == "EUR") and not(body["valuta"] == "USD"))): # controllo che ci siano tutti gli attributi
            return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))
    except:
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token

        risposta = {}
        # in base alla richiesta, eseguo una determinata funzione
        if (request.path == "/buy/"): 
            risposta = query.buy(decodificato["id"]["id"], body["valuta"], body["valore"])
        elif (request.path == "/deposit/"):
            risposta = query.deposit(decodificato["id"]["id"], body["valuta"], body["valore"])
        else:
            risposta = query.withdraw(decodificato["id"]["id"], body["valuta"], body["valore"])

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
    if (not ("data" in body and "valuta" in body) or (not(body["valuta"] == "EUR") and not(body["valuta"] ==  "USD") and not(body["valuta"] ==  ""))): # controllo che ci siano tutti gli attributi
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))
    
    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token
        
        risposta = query.listTransactions(decodificato["id"]["id"], body["valuta"], body["data"])

        return HttpResponse(json.dumps(risposta))
    except Exception as e:
        return HttpResponse(json.dumps({"ridirezione": True, "isTuttoOk":False}))


# endpoint per le richieste al db che richiedono valuta e valore
@api_view(['OPTION', 'POST'])
def uploadImage(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    try:
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token

        risposta = query.updateImage(decodificato["id"]["id"], request.FILES["foto"])

        return HttpResponse(json.dumps(risposta))

    except Exception as e:
        print("aaa: ", e)
        return HttpResponse(json.dumps({"isTuttoOk": False, "ridirezione": True}))


# endpoint per restituire la foto
@api_view(['OPTION', 'POST', 'GET'])
def getImage(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    try: # provo a decodificare il jwt, se non ci riesco vuol dire che non ce
        decodificato = jwt.decode(request.COOKIES["jwt"], "password", algorithms=["HS256"]) # decodifico il token
        

        risposta = query.getImage(decodificato["id"]["id"])

        return FileResponse(risposta)
    except Exception as e:
        return HttpResponse(json.dumps({"ridirezione": True, "isTuttoOk":False}))


# endpoint per restituire il tasso di cambio attuale
@api_view(['OPTION', 'GET'])
def cambio(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml?46f0dd7988932599cb1bcac79a10a16a"
    response = requests.get(url) # contatto il link e trasformo il file xml in un dizionario
    data = xmltodict.parse(response.content)

    cambio = 1
    for valute in data["gesmes:Envelope"]["Cube"]["Cube"]["Cube"]: #cerco i dollari
        if (valute["@currency"] == "USD"):
            cambio = valute["@rate"]
            break

    return HttpResponse(cambio)