import React, {useState} from 'react';
import './App.css';
import Q3 from "./Q3";
import Q4 from "./Q4";
import Q5 from "./Q5";
import VotingComponent from "./vote";
import Q2 from "./Q2";
import ParlementVerteilung from "./torten";
import Vergleich from "./Vergleich";
import ReloadButton from "./ReloadButton";
import Q6 from "./Q6";
import Einkommen from "./Einkommen";


function App() {
    const [view, setView] = useState('home'); // Changed to 'home' for the initial view

    return (
        <div className="App-header">
            {view === 'home' && (
                <>
                    <h1>Wahlinformationssytem 2023</h1>
                    <button onClick={() => setView('analysis')}>Analysis</button>
                    <button onClick={() => setView('voting')}>Voting</button>
                </>
            )}

            {view === 'analysis' && (
                <>
                    <button onClick={() => setView('home')}>Home</button>
                    <ReloadButton/>
                    <div style={{height: '20px'}}/>

                    <h5>Pie Chart</h5>
                    <ParlementVerteilung/>
                    <div style={{height: '20px'}}/>

                    <h5>Q2</h5>
                    <Q2/>
                    <div style={{height: '20px'}}/>

                    <h5>Q3</h5>
                    <Q3/>
                    <div style={{height: '20px'}}/>

                    <h5>Q4</h5>
                    <Q4/>
                    <div style={{height: '20px'}}/>

                    <h5>Q5</h5>
                    <Q5/>
                    <div style={{height: '20px'}}/>

                    <h5>Q6</h5>
                    <Q6/>
                    <div style={{height: '20px'}}/>

                    <h5>Einkommen und Wahlergebnisse</h5>
                    <Einkommen/>
                    <div style={{height: '20px'}}/>

                    <h5>Vergleich mit Wahlergebnissen 2018</h5>
                    <Vergleich/>
                    <div style={{height: '20px'}}/>

                </>
            )}

            {view === 'voting' && (
                <>
                    <button onClick={() => setView('home')}>Home</button>
                    <VotingComponent/>
                </>
            )}
        </div>
    );
}

export default App;