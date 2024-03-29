from rest_framework.decorators import api_view
from django.http import  HttpResponse
from db.query import Query # importo le query al db
import json
import jwt
from . import views
#from datetime import date
import datetime
query = Query()

# endpoint per il login
@api_view(['OPTION', 'POST'])
def login(request):
    if (str(request.method) == 'OPTION'): # se è il preflight
        return HttpResponse("option")

    body = views.controlla_corpo(request) # controllo sia un json
    if (body == False):
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    # controllo gli attributi
    if (not ("password" in body and "email" in body)): # controllo che ci siano tutti gli attributi
        return HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))

    [rispostaDb, id] = query.login(body)
    response = HttpResponse(json.dumps(rispostaDb)) # effettuo il login
    if (id): # se c'è l'id vuol dire che sono loggato e posso creare il jwt
        token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=900), "id": id}, "password")#, "data": int(datetime.datetime.utcnow())}, "password") # crea il jwt che dura per 15 minuti
        response.set_cookie('jwt', token, max_age=900, httponly='true') # setta il cookie jwt che dura per massimo 15 minuti in modo httponly

    return response