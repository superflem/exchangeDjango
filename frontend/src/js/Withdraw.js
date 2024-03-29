import '../css/Form.css';
import axios from 'axios';
import {useState} from 'react';
import {controllaSoldi, controllaValuta} from './Buy';

const Withdraw = (props) => {

    const euro = props.euro;
    const dollari = props.dollari;
    const [max, setMax] = useState(dollari);

    const handleLoginForm = async (e) => {
        e.preventDefault(); //evita di ricaricare la pagina
        const url = "http://localhost:8000/withdraw/";

        const valore = e.target.valore.value;
        const valuta = e.target.valuta.value;

        // prendo il massimo valore che posso comprare
        let max = 0;
        if (valuta === "EUR")
            max = euro;
        else
            max = dollari;

        if (!controllaSoldi(valore, max)) { // controlla i soldi
            alert("Non hai inserito correttamente i soldi");
            return;
        }

        if (!controllaValuta(valuta)) { // controlla la valuta
            alert("Non hai inserito correttamente la valuta");
            return;
        }

        const corpo = {
            valore: valore,
            valuta: valuta
        };

        const risposta = await axios.post(url, corpo);
        const oggetto = risposta.data;

        if (oggetto["ridirezione"]) {
            alert('Sessione scaduta');
            window.location.href = 'http://localhost:3000/';
        }
        else {
            alert (oggetto["messaggio"]);
            if (oggetto["isTuttoOk"])
            {
                window.location.href = 'http://localhost:3000/home';
            }
        }
    }

    function cambiaMassimo(e) { //cambio il massimo di soldi nella form in base alla valuta
        if (e.target.value === 'EUR')
            setMax(euro);
        
        else
            setMax(dollari);
        
    }

    return (
        <div className="divForm">
            <h1>Deposito Sul Conto Corrente</h1>

            <form id = "form" onSubmit = {handleLoginForm}>
                <input className='testo' type='number' id='valore' name='valore' placeholder='Valore da depositare' min='1' max={max} step="0.01" required /> <br /> <br />
                
                <select id="valuta" name="valuta" form='form' onChange={cambiaMassimo}>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                </select> <br /> <br />
                <input id='bottoneInterno' type='submit'/>
            </form>
        </div> 
    );
}
 
export default Withdraw;