import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';

import { List, ListItem, ListItemText } from '@material-ui/core';

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

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
    <Button variant="contained" color="primary">
      Click
    </Button>
        </a>
          <MyComponent/>
      </header>
    </div>
  );
}

export default App;
