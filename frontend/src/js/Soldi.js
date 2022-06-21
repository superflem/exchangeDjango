import '../css/Soldi.css';

const Soldi = (props) => {
    const euro = props.euro; 
    const dollari = props.dollari;   
    return (
        <nav className="navbar">
            <div className="divLink">
                <label className="soldii" id="euro">{euro} €</label>
                <label className="soldii" id="dollari">{dollari} $</label>
            </div>
        </nav>
    );

}
 
export default Soldi;