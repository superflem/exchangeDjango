import axios from 'axios';
import {useEffect} from 'react';
import {useState} from 'react';


const Cambio = () => {

    const [tasso, setTasso] = useState(0)

    return (
        <div className='cambio'>
            <h1>1 € equivale ad {tasso} $</h1>
        </div>
    )
}

export default Cambio;


