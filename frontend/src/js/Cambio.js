import axios from 'axios';
import {useEffect} from 'react';
import {useState} from 'react';
axios.defaults.withCredentials = true;



const Cambio = () => {

    const [tasso, setTasso] = useState(0)

    useEffect(async () => { //una volta caricata la pagina, controllo che il token sia valido e inserisco i valori dei soldi nella pagina html
        const url = "http://localhost:8000/cambio/";
        const risposta = await axios.get(url);

        setTasso(risposta.data);

    }, []);

    return (
        <div className='cambio'>
            <h1>1 € equivale ad {tasso} $</h1>
        </div>
    )
}

export default Cambio;


