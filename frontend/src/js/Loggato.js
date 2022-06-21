import {BrowserRouter as Router, Route, Switch} from 'react-router-dom'; //servono per andare in diverse pagine
import Home from './Home';
import NavbarLoggato from './NavbarLoggato';
import Soldi from './Soldi';
import Deposito from './Deposito';
import Withdraw from './Withdraw';
import Buy from './Buy';
import ListTransactions from './ListTransactions';
import axios from 'axios';
import {useEffect} from 'react';
import {useState} from 'react';

const Loggato = () => {
    //let nome = '';
    const [nome, setNome] = useState('');
    const [euro, setEuro] = useState(0);
    const [dollari, setDollari] = useState(0);
    const [getFoto, setGetFoto] = useState(null);

    useEffect(async () =>{ //una volta caricata la pagina, controllo che il token sia valido e inserisco i valori dei soldi nella pagina html
        const url = "http://localhost:8000/query/";
        const risposta = await axios.post(url);
        //const oggetto = JSON.parse(risposta.data);
        const oggetto = risposta.data;

        if (oggetto["ridirezione"])
        {
            alert('Sessione scaduta');
            window.location.href = 'http://localhost:3000/';
        }
        else
        {
            if (oggetto["isTuttoOk"]) 
            {
                setNome(oggetto["nome"][0].toUpperCase() + oggetto["nome"].slice(1)); //metto la prima lettera maiuscola
                setEuro(Number(oggetto["euro"]).toFixed(2));
                setDollari(Number(oggetto["dollari"]).toFixed(2));
            }
            else
            {
                alert(oggetto["messaggio"]);
            }
        }

        // prendo la foto profilo
        const url2 = "http://localhost:8000/getImage/";
        const risposta2 = await axios.get(url2, {responseType: "blob"});
        getBase64(risposta2.data, (foto) => {setGetFoto(foto)});
    });

    function getBase64(file, cb) {
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
            cb(reader.result)
        };
        reader.onerror = function (error) {
            console.log('Error: ', error);
        };
    }

    

    return (
        <Router>
            <div className="loggato">
                <NavbarLoggato />
                <Soldi euro={euro} dollari={dollari}/>

                <Switch>
                    <Route exact path='/home'>
                        <Home nome={nome} foto={getFoto}/>
                    </Route>

                    <Route exact path='/deposit'>
                        <Deposito />
                    </Route>

                    <Route exact path='/withdraw'>
                        <Withdraw euro={euro} dollari={dollari}/>
                    </Route>

                    <Route exact path='/buy'>
                        <Buy euro={euro} dollari={dollari}/>
                    </Route>

                    <Route exact path='/listTransactions'>
                        <ListTransactions />
                    </Route>
                </Switch>
                
            </div>
        </Router>
    );
}
export default Loggato;