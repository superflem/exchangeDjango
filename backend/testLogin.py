# coding: utf-8

from django.test import TestCase
from backend.view_login import login
from django.http import  HttpResponse, HttpRequest
import json
from db.signup import Signup

class testLogin(TestCase):

    # inizializzo il test
    def setUp(self):
        self.login = login

    # controllo gli input del metodo
    def testInput(self):
        # provo il get
        request = HttpRequest()
        request.method = "GET"
        self.assertEqual(405, self.login(request).status_code, "test usando il get")

        # provo option 
        request.method = "OPTION"
        response = self.login(request)
        rispostaAttesa = HttpResponse("option")
        self.assertEqual(rispostaAttesa.content, response.content, "test usando l'option")

        # provo post ma con un body che non è json
        request2 = HttpRequest()
        request2.method = "POST"
        request2._body = "ciao"
        response = self.login(request2)
        rispostaAttesa = HttpResponse(json.dumps({"isTuttoOk":False, "errore":"formato della richiesta non corretta"}))
        self.assertEqual(rispostaAttesa.content, response.content, "test usando un body non json")

        # provo con un body senza niente
        request2._body = json.dumps({})
        response = self.login(request2)
        self.assertEqual(rispostaAttesa.content, response.content, "test usando un body non json")
        
        # provo con un body senza email
        request2._body = b'"password": "prova"}'
        response = self.login(request2)
        self.assertEqual(rispostaAttesa.content, response.content, "test usando un body non json")

        # provo con un body senza password
        request2._body = b'"email": "prova@prova"}'
        response = self.login(request2)
        self.assertEqual(rispostaAttesa.content, response.content, "test usando un body non json")

    # inserisco una mail che non esiste nel db
    def testEmailNonEsistente(self):
        request2 = HttpRequest()
        request2.method = "POST"
        request2._body = b'{"email": "prova@gmail.it", "password": "pippo"}'

        response = self.login(request2)
        rispostaAttesa = HttpResponse(json.dumps({"isTuttoOk": False, "messaggio": "Email o password non corretti"}))
        self.assertEqual(rispostaAttesa.content, response.content, "test usando un mail non valida")

    # inserisco una mail corretta ma una password sbagliata
    def testPasswordSbagliata(self):
        signup = Signup()
        signup.signup({"nome":"mario", "cognome": "rossi", "iban": "IT0000000000000000000000001", "email": "prova@gmail.com", "password": "3ab27885d805eaf430d9a659bbfb76e88ac4d0d8cf6053a40fd96006dc5718c91935fe7928fb1bb1c1c9870298b45702d76ad1a384eddb56e3ac971cd5075488"})

        request2 = HttpRequest()
        request2.method = "POST"
        request2._body = b'{"email": "prova@gmail.it", "password": "pippo"}'

        response = self.login(request2)
        rispostaAttesa = HttpResponse(json.dumps({"isTuttoOk": False, "messaggio": "Email o password non corretti"}))
        self.assertEqual(rispostaAttesa.content, response.content, "test usando una password non valida")

    # login con successo
    def testLoginGiusto(self):
        signup = Signup()
        signup.signup({"nome":"mario", "cognome": "rossi", "iban": "IT0000000000000000000000001", "email": "prova@gmail.com", "password": "3ab27885d805eaf430d9a659bbfb76e88ac4d0d8cf6053a40fd96006dc5718c91935fe7928fb1bb1c1c9870298b45702d76ad1a384eddb56e3ac971cd5075488"})

        request2 = HttpRequest()
        request2.method = "POST"
        request2._body = b'{"email": "prova@gmail.com", "password": "3ab27885d805eaf430d9a659bbfb76e88ac4d0d8cf6053a40fd96006dc5718c91935fe7928fb1bb1c1c9870298b45702d76ad1a384eddb56e3ac971cd5075488"}'

        response = self.login(request2)
        rispostaAttesa = HttpResponse(json.dumps({"isTuttoOk": True, "messaggio": "Autenticazione avvenuta"}))
        self.assertEqual(rispostaAttesa.content, response.content, "test usando una mail e una password corretti")
