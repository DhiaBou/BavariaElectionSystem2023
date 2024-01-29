import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';

import {List, ListItem, ListItemText} from '@material-ui/core';
import Q3 from "./Q3";
import Q4 from "./Q4";
import Q5 from "./Q5";
import VotingComponent from "./vote";
import Q2 from "./Q2";
import ParlementVerteilung from "./torten";
import Vergleich from "./Vergleich";
import ReloadButton from "./ReloadButton";

const BackendHealthComponent = () => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis')
            .then(response => response.json())
            .then(data => setItems(data))
            .catch(error => console.error("There was an error!", error));
    }, []);

    console.log(
        items
    );

    return (
        <List>
            {items.map((item, index) => (
                <ListItem key={index}>
                    <ListItemText primary={item}/>
                </ListItem>
            ))}
        </List>
    );
}

function App() {
    const [view, setView] = useState('home'); // Changed to 'home' for the initial view

    return (
        <div className="App-header">
            {view === 'home' && (
                <>
                    <img src={logo} className="App-logo" alt="logo"/> {/* Logo */}
                    <button onClick={() => setView('analysis')}>Analysis</button>
                    <button onClick={() => setView('voting')}>Voting</button>
                </>
            )}

            {view === 'analysis' && (
                <>
                    <button onClick={() => setView('home')}>Home</button>
                    <ReloadButton/>
                    {/* Home Button */}
                    <BackendHealthComponent/>
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

                    <h5>Vergleich mit Wahlergebnissen 2018</h5>
                    <Vergleich/>
                    <div style={{height: '20px'}}/>

                </>
            )}

            {view === 'voting' && (
                <>
                    <button onClick={() => setView('home')}>Home</button>
                    {/* Home Button */}
                    <VotingComponent/>
                </>
            )}
        </div>
    );
}

export default App;