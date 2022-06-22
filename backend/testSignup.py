# coding: utf-8

# import unittest
from django.test import TestCase
from db.signup import Signup

class testSignup(TestCase):

    # inizializzo il test
    def setUp(self):
        self.Signup = Signup()

    # controllo che sia effettivamente un oggetto ditipo signup (consistenza architetturale)
    def testOggetto(self):
        self.assertTrue(isinstance(self.Signup, Signup), "self.signup non è un oggetto Signup")

   # controllo gli input del metodo
    def testInput(self):
        body = {"nome": "mario", "cognome": "perna", "email":"mario.pernagmail.com", "iban":"IT00000000000000000000000033", "password": "acd3a2ca97dd545afc16ccb52e497d42a0a05342215c15d5e4f56ccc69ab7e947bf98353b57a3cad8b2268714aae4ae7ac8653dee473a3d0a71c32e8da4d174"}

        risposta1 = {"isTuttoOk": False, "messaggio": "L'iban non ha il numero di caratteri giusto"}
        risposta2 = {"isTuttoOk": False, "messaggio": "L'indirizzo email non è valido"}
        risposta3 = {"isTuttoOk": False, "messaggio": "La password non è nel formato corretto"}

        self.assertEqual(risposta1, self.Signup.signup(body), "Errore nel controllo dell'iban")

        body["iban"] = "IT0000000000000000000000003"
        self.assertEqual(risposta2, self.Signup.signup(body), "Errore nel controllo della email")

        body["email"] = "mario.perna@gmail.com"
        self.assertEqual(risposta3, self.Signup.signup(body), "Errore nel controllo della password")

    # controllo l'output del metodo prima inserendo un utente e poi rimettendo la stessa email
    def testInserimento1(self):
        # il primo è positivo
        body = {"nome": "mario", "cognome": "perna", "email":"mario.perna@gmail.com", "iban":"IT0000000000000000000000003", "password": "acd3a2ca97dd545afc16ccb52e497d42a0a05342215c15d5e4f56ccc69ab7e947bf98353b57a3cad8b2268714aae4ae7ac8653dee473a3d0a71c32e8da4d174b"}
        risultato = {"isTuttoOk": True, "messaggio": "Utente inserito correttamente"}
        
        self.assertEqual(risultato, self.Signup.signup(body), "Errore nell'inserimento nel db") # test che inserisce

        body["iban"] = "IT0000000000000000000032003"
        risultato = {"isTuttoOk": False, "messaggio": "Email già in uso"}
        self.assertEqual(risultato, self.Signup.signup(body), "Errore nel controllo della mail sul db") # inserisco una mail già esistente

        

    # controllo l'output del metodo prima inserendo un utente e poi rimettendo lo stesso iban
    def testInserimento1(self):
        # il primo è positivo
        body = {"nome": "mario", "cognome": "perna", "email":"mario.perna@gmail.com", "iban":"IT0000000000000000000000003", "password": "acd3a2ca97dd545afc16ccb52e497d42a0a05342215c15d5e4f56ccc69ab7e947bf98353b57a3cad8b2268714aae4ae7ac8653dee473a3d0a71c32e8da4d174b"}
        risultato = {"isTuttoOk": True, "messaggio": "Utente inserito correttamente"}
        
        self.assertEqual(risultato, self.Signup.signup(body), "Errore nell'inserimento nel db") # test che inserisce

        body["email"] = "prova.prv@fallita.it"
        risultato = {"isTuttoOk": False, "messaggio": "IBAN già in uso"}
        self.assertEqual(risultato, self.Signup.signup(body), "Errore nel controllo della mail sul db") # inserisco un iban  già esistente


    # metodi invocabili (coerenza funzionale)
    def testFunzione(self):
	    self.assertTrue(callable(self.Signup.signup), "self.signup non ha il metodo signup(self, body)")