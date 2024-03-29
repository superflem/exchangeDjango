import '../css/Form.css';
import {useState} from 'react';
import axios from 'axios';

export const controllaSoldi = (soldi = 0, max = 0) => { // controllo che i soldi siano dei numeri > di zero
    if (parseFloat(soldi)+"" === "NaN")
        return false;
    
    if (max === -1)
        max = parseFloat(soldi)+2;
    
    if (parseFloat(soldi) <= 0 || parseFloat(soldi) > max)
        return false;
    return true;
}

export const controllaValuta = (valuta = "") => { // controllo della valuta
    if (valuta === "USD" || valuta === "EUR")
        return true;
    return false;
}


const Buy = (props) => {

    const euro = props.euro;
    const dollari = props.dollari;
    const [max, setMax] = useState(dollari);

    const handleLoginForm = async (e) => {
        e.preventDefault(); //evita di ricaricare la pagina
        const url = "http://localhost:8000/buy/";

        const quantita_spesa = e.target.valore.value;
        const valuta = e.target.valuta.value;

        // prendo il massimo valore che posso comprare
        let max = 0;
        if (valuta === "EUR")
            max = euro;
        else
            max = dollari;

        if (!controllaSoldi(quantita_spesa, max)) { // controlla i soldi
            alert("Non hai inserito correttamente i soldi");
            return;
        }

        if (!controllaValuta(valuta)) { // controlla la valuta
            alert("Non hai inserito correttamente la valuta");
            return;
        }



        const corpo = {
            valore: quantita_spesa,
            valuta: valuta
        };

        const risposta = await axios.post(url, corpo);
        const oggetto = risposta.data;

        if (oggetto["ridirezione"]) {
            alert('Sessione scaduta');
            window.location.href = 'http://localhost:3000/';
        }
        else {
            if (oggetto["messaggio"] === undefined)
                alert("Errore inatteso, prova a togliere un centesimo");
            else {
                alert (oggetto["messaggio"]);
                if (oggetto["isTuttoOk"])
                    window.location.href = 'http://localhost:3000/home';
            }
        }
    }

    function cambiaMassimo(e) { //cambio del massimo nella form in base alla valuta selezionata
        if (e.target.value === 'EUR')
            setMax(euro);
        
        else   
            setMax(dollari);
    }

    return (
        <div className="divForm">
            <h1>Converti Valuta</h1>

            <form id = "form" onSubmit = {handleLoginForm}>
                <input className='testo' type='number' id='valore' name='valore' placeholder="Valore da convertire nell'altra valuta" min='1' max={max} step="0.01" required/><br /><br />
                
                <select id="valuta" name="valuta" form='form' onChange={cambiaMassimo}>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                </select> <br /> <br />
                <input id='bottoneInterno' type='submit'/>
            </form>
        </div> 
    );
}
 
export default Buy;