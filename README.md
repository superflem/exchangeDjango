# Per eseguire il frontend è necessario avere installato NodeJs: https://nodejs.dev/

## BACKEND
Nella cartella di root del backend lanciare il seguente comando:

### `pipenv shell`
Si entra nell'ambiente virtuale di Django. Poi lanciare i seguenti comandi:


#### `pipenv install`
Installa le dipendenzepresenti nel Pipfile

#### `python manage.py runserver`
Lancia il backend

#### `python manage.py test`
Esegue i test

----


## FRONTEND
Nella cartella di root del frontend, lanciare i seguenti comandi:

### `npm install`
Installa tutti i moduli necessari presenti in package.json per eseguire i file

### `npm start`
Esegue l'applicazione React. Apri [http://localhost:3000](http://localhost:3000) nel browser.
Se non funziona, lanciarlo da amministratore

### `npm test`
Esegue i test presenti nella cartella /src/test

----

Per fare l'accesso come admin in Django, andare su [http://localhost:8000/admin](http://localhost:8000/admin) e inserire come username `root` e come password `root`

### IMPORTANTE
Non usare il server di Django mentre si è loggati come utente `root`, fare prima il logout
