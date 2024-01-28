import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';

import { List, ListItem, ListItemText } from '@material-ui/core';
import MyPieChart from "./torten";
import ProductList from "./list";
import ProductListt from "./q3";
import Listq4 from "./q4";
import Listq5 from "./q5";
import VotingComponent from "./vote";

const MyComponent = () => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/')
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
                    <ListItemText primary={item} />
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
          <img src={logo} className="App-logo" alt="logo" /> {/* Logo */}
          <button onClick={() => setView('analysis')}>Analysis</button>
          <button onClick={() => setView('voting')}>Voting</button>
        </>
      )}

      {view === 'analysis' && (
        <>
          <button onClick={() => setView('home')}>Home</button> {/* Home Button */}
          <MyComponent />
                     <div style={{ height: '20px' }} />
<h5>Pie Chart</h5>
          <MyPieChart />
                     <div style={{ height: '20px' }} />
<h5>Q2</h5>

          <ProductList />
                     <div style={{ height: '20px' }} />
<h5>Q3</h5>

          <ProductListt />
                     <div style={{ height: '20px' }} />
<h5>Q4</h5>

          <Listq4 />
                     <div style={{ height: '20px' }} />
<h5>Q5</h5>

          <Listq5 />         <div style={{ height: '20px' }} />

        </>
      )}

      {view === 'voting' && (
        <>
          <button onClick={() => setView('home')}>Home</button> {/* Home Button */}
          <VotingComponent />
        </>
      )}
    </div>
  );
}

export default App;