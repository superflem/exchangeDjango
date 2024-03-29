import { sha3_512 } from 'js-sha3';
import { useRef } from 'react';
import '../css/Form.css';
import axios from 'axios';
axios.defaults.withCredentials = true;

export const controllaEmail = (input = "") => input.includes("@"); // controlla che l'input della mail abbia la chiocciola
export const controllaPassword = (input = "") => input.length === 128; // controlla che l'input della mail abbia la chiocciola

const Login = () => {
    //servono per inviare i dati nel form
    const emailInput = useRef();
    const passwordInput = useRef();

    const handleLoginForm = async (e) => {
        e.preventDefault(); //evita di ricaricare la pagina
        const url = "http://localhost:8000/login/";
        const email = emailInput.current.value;
        let password = passwordInput.current.value;
        password = sha3_512(password); //cifro la password

        // controllo la email
        if (!controllaEmail(email)) {
            alert("La email non è valida");
            return;
        }

        // controllo la password
        if (!controllaPassword(password)) {
            alert("La password non è valida");
            return;
        }

        const corpo = {email: email, password: password, withCredentials: true}; //creo l'oggetto json da inviare al server
        
        //INVIO I DATI
        const risposta = await axios.post(url, corpo);
        const oggetto = risposta.data;
        if (!oggetto["isTuttoOk"]) //se c'è un errore lo comunico, altrimenti procedo
            alert(oggetto["messaggio"]);
        
        else { //se avviene con successo il login
            alert("Autenticazione avvenuta");
            const link = window.location.href + 'home'; //rimando alla pagina principale di login
            window.location.replace(link);
            //axios.post("http://localhost:80/ciaoo", {email: email, password: password, withCredentials: true});
        }
    }

    return (
        <div className="divLogin">
            <h1>Login</h1>

            <form onSubmit = {handleLoginForm}>
                <input className='testo' type='text' ref={emailInput} id='email' name='email' placeholder='Email' required /> <br /> <br />
                <input className='testo' type='password' ref={passwordInput} id='password' name='password' placeholder='Password' required /> <br /> <br />
                <button id='bottone' type='submit'> Invia</button>
            </form>
        </div> 
    );
}
 
export default Login;