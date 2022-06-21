import '../css/Home.css';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
axios.defaults.withCredentials = true;

const Home = (props) => {
    const nome = props.nome;
    const getFoto = props.foto;

    const [foto, setFoto] = useState();
    const [descrizione, setDescrizione] = useState("Scegli un'immagine");

    const handleLoginForm = async (e) => {
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

            {   !!getFoto && 
                <img id="foto" src={getFoto} alt="Foto profilo"/>
            }

            <form encType="multipart/form-data" onSubmit = {handleLoginForm}>
                <br />
                <div id="divFile">
                    <label id="labelFile" htmlFor="file">
                        Scegli
                        <input id="file" accept="image/png, image/jpg, image/gif, image/jpeg" type="file" onChange={e => {setFoto(e.target.files[0]); setDescrizione(e.target.files[0].name);}}/>
                    </label>
                    <span id="spanFile">
                        {descrizione}
                    </span>
                </div>
                <br />
                <br />

                <button id='bottone' type='submit'> Invia</button>
                
            </form>   
            <br />         
        </div> 
    );
}
 
export default Home;