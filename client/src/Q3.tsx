import React, {useEffect, useState} from 'react';
import {FormControl, MenuItem, Select, SelectChangeEvent} from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

interface BackendResponse {
    stimmkreisid: string;
    parteiname: string;
    wahlbeteiligung: string;
    gesamt_stimmen: number;
    percentage: string;
    gewaehlte_kandidaten: string;
    erststimmen: string;
    zweite_stimme: string;
}

interface ProductTableProps {
    filteredData: BackendResponse[]; // Assuming 'BackendResponse' is your data type
}

const ProductTable: React.FC<ProductTableProps> = ({filteredData}) => {
    return (
        <TableContainer component={Paper}>
            <Table sx={{minWidth: 650}} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Parteinamen</TableCell>
                        <TableCell>Erststimmen</TableCell>
                        <TableCell>Zweitstimmen</TableCell>
                        <TableCell>Gesamte Stimmen</TableCell>
                        <TableCell>Prozentsatz</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {    // @ts-ignore
                        filteredData.map((row) => (
                            <TableRow
                                key={row.stimmkreisid + row.parteiname}
                                sx={{'&:last-child td, &:last-child th': {border: 0}}}
                            >
                                <TableCell>{row.parteiname}</TableCell>
                                <TableCell>{row.erststimmen}</TableCell>
                                <TableCell>{row.zweite_stimme}</TableCell>
                                <TableCell>{row.gesamt_stimmen}</TableCell>
                                <TableCell>{row.percentage}</TableCell>
                            </TableRow>
                        ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Q3 = () => {
    const [backendData, setBackendData] = useState<BackendResponse[]>([]);
    const [selectedId, setSelectedId] = useState('');

    // Fetch data from the server
    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q3')
            .then(response => response.json())
            .then(data => setBackendData(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    const ids = Array.from(new Set(backendData.map(row => row.stimmkreisid)));

    const handleSelectionChange = (event: SelectChangeEvent<string>) => {
        const newSelectedProductId = event.target.value as string;
        setSelectedId(newSelectedProductId);
    };

    const filteredData = backendData.filter(row => row.stimmkreisid === selectedId)
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
                        Stimmkreiswählen
                    </MenuItem>
                    {ids.map(id => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            {filteredData && filteredData[0] && filteredData[0].wahlbeteiligung !== undefined &&
                <>
                    <a style={{fontSize: 'smaller'}}>Wahlbeteiligung: {filteredData[0].wahlbeteiligung}%</a> <br/>
                    <a style={{fontSize: 'smaller'}}>Gewählte
                        Kandidaten: {filteredData[0].gewaehlte_kandidaten} - {filteredData[0].parteiname}</a>
                </>
            }
            <ProductTable filteredData={filteredData}/>
        </div>
    );
}
export default Q3;
