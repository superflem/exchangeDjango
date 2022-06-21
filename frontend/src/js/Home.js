import '../css/Home.css';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
axios.defaults.withCredentials = true;

const Home = (props) => {
    const nome = props.nome;
    const getFoto = props.foto;

    const [foto, setFoto] = useState();

    
    // const [getFoto, setGetFoto] = useState(null);

    // useEffect(async () => { //una volta caricata la pagina, controllo che il token sia valido e inserisco i valori dei soldi nella pagina html
    //     const url = "http://localhost:8000/getImage/";

    //     const risposta = await axios.get(url, {responseType: "blob"});

    //     getBase64(risposta.data, (foto) => {setGetFoto(foto)});
    // }, []);
    

    
    const handleLoginForm = async (e) => {
        //e.preventDefault(); //evita di ricaricare la pagina

        const url = "http://localhost:8000/uploadImage/";

        const dati = new FormData();
        
        dati.append("foto", foto, foto.name);
        
        const body = {method: "post", url: url, data: dati, withCredentials: true, headers: { "Content-Type": "multipart/form-data" }}
        const risposta = await axios (url, body);
        const oggetto = risposta.data;
        alert(oggetto.messaggio)
    }

    return (
        <div className="divHome">
            <h1>Benvenuto</h1>
            <h2>{nome}</h2>

            <form encType="multipart/form-data" onSubmit = {handleLoginForm}>

            {/*<form encType="multipart/form-data" method="post" action="http://localhost:8000/uploadImage/">*/}
                <input type="file" onChange={e => setFoto(e.target.files[0])}/>
                <button id='bottone' type='submit'> Invia</button>
            </form>
            {   !!getFoto && 
                <img src={getFoto} alt="ciao"/>
            }

            
        </div> 
        


    );
}
 
export default Home;