import React, {useEffect, useState} from 'react';
import {FormControl, List, ListItem, MenuItem, Select, SelectChangeEvent} from '@mui/material';

interface BackendResponse {
    kandidat: string;
    kurzbezeichnung: string;
}

const Q2 = () => {
    const [backendData, setBackendData] = useState<BackendResponse[]>([]);
    const [selectedId, setSelectedId] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q2')
            .then(response => response.json())
            .then(data => setBackendData(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    const ids = Array.from(new Set(backendData.map(row => row.kurzbezeichnung)));

    const handleSelectionChange = (event: SelectChangeEvent<string>) => {
        setSelectedId(event.target.value as string);
    };

    const filteredData = backendData.filter(row => row.kurzbezeichnung === selectedId);

    return (
        <div>
            <FormControl fullWidth>
                <Select
                    value={selectedId}
                    onChange={handleSelectionChange}
                    displayEmpty
                    inputProps={{'aria-label': 'Without label'}}
                >
                    <MenuItem value="" disabled>
                        Partei Wählen
                    </MenuItem>
                    {ids.map(id => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            <List style={{maxHeight: '50vh', overflow: 'auto'}}>
                {filteredData.map((row, index) => (
                    <ListItem key={index}>{row.kandidat}</ListItem>
                ))}
            </List>
        </div>
    );
};

export default Q2;
