import '../css/Form.css';
import '../css/ListTransactions.css';
import {useEffect} from 'react';
import {useState} from 'react';
import axios from 'axios';
import {controllaValuta} from './Buy';
const parse = require('html-react-parser');

export const controllaData = (data = "") => { // controllo della data
    if (data === "") // la data può essere vuota
        return true;

    if (data.length !== 10) // controllo la dimensione
        return false;

    if (parseInt(data.substring(0, 4))+"" === "NaN") // controllo l'anno
        return false;

    if (parseInt(data.substring(5, 7))+"" === "NaN") // controllo il mese
        return false;

    if (parseInt(data.substring(8, 10))+"" === "NaN") // controllo il giorno
        return false;

    if (data.charAt(4) !== '-' && data.charAt(7) !== '-') // controllo i trattini
        return false;

    return true;
}

const ListTransactions = () => {

    const [tabella, setTabella] = useState('');
    const url = "http://localhost:8000/listTransactions/";

    useEffect(async () =>{ //una volta caricata la pagina, controllo che il token sia valido e inserisco i valori dei soldi nella pagina html
        const posizioneValuta = window.location.href.indexOf('valuta='); //prendo il valore della valuta
        let valuta = '';
        if (posizioneValuta != -1)
            valuta = window.location.href.slice(posizioneValuta+7, posizioneValuta+5+5);
        

        const posizioneData = window.location.href.indexOf('data='); //prendo il valore della data
        let data = '';
        if (posizioneData != -1)
            data = window.location.href.slice(posizioneData+5, posizioneData+5+10);
        

        const corpo = {
            valuta: valuta,
            data: data
        };

        const risposta = await axios.post(url, corpo);
        const oggetto = risposta.data;
        
        if (oggetto["ridirezione"]) {
            alert('Sessione scaduta');
            window.location.href = 'http://localhost:3000/';
        }
        else {
            if (oggetto["isTuttoOk"])  {
                if (oggetto["listaTransizioni"] != '[]')
                    creaTabella(oggetto["listaTransizioni"]); //creo la tabella 
            }
            else
                alert(oggetto["messaggio"]);   
        }
    });

    function creaTabella (lista) {
        let nuovaTabella = '';
        let valutaComprata = '';
        let valutaSpesa = '';
        for (let i = 0; i < lista.length; i++) {
            if (i%2 == 1) //guardo se devo fare lo sfondo bianco o grigio
                nuovaTabella = nuovaTabella + '<tr>';
            
            else
                nuovaTabella = nuovaTabella + '<tr className = "dispari">';
            
            if (lista[i]["valuta_comprata"] == 'USD') { //setto le valute
                valutaComprata = '$';
                valutaSpesa = '€';
            }
            else {
                valutaComprata = '€';
                valutaSpesa = '$';
            }

            nuovaTabella = nuovaTabella + '<td>' + lista[i]["quantita_spesa"].toFixed(2) + " " + valutaSpesa + "</td>"; //spesa
            nuovaTabella = nuovaTabella + '<td>' + lista[i]["quantita_comprata"].toFixed(2) + " " + valutaComprata + "</td>"; //comprata
            nuovaTabella = nuovaTabella + '<td>' + giraData(lista[i]["data"]) + "</td>"; //data
            //nuovaTabella = nuovaTabella + '<td>' + lista[i]["data"] + "</td>"; //data
            nuovaTabella = nuovaTabella + '</tr>';
        }
        setTabella(nuovaTabella);
    }

    function giraData(data) {
       //trasformo da anno mese giorno a giorno mese anno
        return data.slice(8, 10)+'-'+data.slice(5, 7)+'-'+data.slice(0, 4);
    }

    const handleLoginForm = async (e) => {
        e.preventDefault();
        const data = e.target.data.value;
        const valuta = e.target.valuta.value;

        if (valuta !== "" && !controllaValuta(valuta)) { // controlla la valuta
            alert("Non hai inserito correttamente la valuta");
            return;
        }

        if (data !== "" && !controllaData(data)) { 
            alert("Non hai inserito correttamente la valuta"); // controllo della data
            return;
        }

        let nuovaQuery = 'http://localhost:3000/listTransactions';
        if (data!='' || valuta!='') {
            nuovaQuery = nuovaQuery+'?'
            if (data!='' && valuta!='')
                nuovaQuery = nuovaQuery+'data='+data+'&valuta='+valuta;
            
            else if (data!='')
                nuovaQuery = nuovaQuery+'data='+data;
            
            else
                nuovaQuery = nuovaQuery+'valuta='+valuta;
        }
        window.location.href = nuovaQuery;
    }

    return (
        <div className="listTransactions">
            <h1>Storico delle transizioni</h1>

            <table>
                <thead>
                    <tr>
                        <th>Quantita Spesa</th>
                        <th>Quantita Comprata</th>
                        <th>Data</th>
                    </tr>
                </thead>
                <tbody>
                    {parse(tabella) /* creo la tabella*/ }
                </tbody>
            </table>
            
            <h2>Filtri</h2>
            <form id = "form" onSubmit = {handleLoginForm}>
                <input type="date" id="data" name="data" /> <br /> <br />

                <select id="valuta" name="valuta" form='form'>
                    <option value="">Nessuna</option>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                </select> <br /> <br />
                <input id='bottoneInterno' type='submit'/>
            </form>
        </div> 
    );
}
 
export default ListTransactions;