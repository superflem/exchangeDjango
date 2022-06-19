import '../css/Home.css';
import axios from 'axios';
axios.defaults.withCredentials = true;

const Home = (props) => {
    const nome = props.nome;

    const handleLoginForm = async (e) => {
        const url = "http://localhost:8000/uploadImage/";
    }

    return (
        <div className="divHome">
            <h1>Benvenuto</h1>
            <h2>{nome}</h2>

            <form onSubmit = {handleLoginForm}>
                <input type="file" />
                <button id='bottone' type='submit'> Invia</button>
            </form>

            
        </div> 
        


    );
}
 
export default Home;