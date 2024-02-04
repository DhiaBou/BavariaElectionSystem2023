import React, {useEffect, useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {FormControl, MenuItem, Select, SelectChangeEvent} from "@mui/material";

interface BackendResponse {
    kurzbezeichnung: string;
    name: string;
    stimmkreisid: string;
    distance: number;
    rn: number;
    winner_or_loser: string;
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
                        <TableCell>Partei</TableCell>
                        <TableCell>Kandidatenname</TableCell>
                        <TableCell>Stimmkreis</TableCell>
                        <TableCell>Distanz zum nächsten oder zum ersten</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredData.map((row) => (
                        <TableRow
                            sx={{'&:last-child td, &:last-child th': {border: 0}}}
                        >
                            <TableCell component="th" scope="row">
                                {row.kurzbezeichnung}
                            </TableCell>
                            <TableCell component="th" scope="row">
                                {row.name}
                            </TableCell>
                            <TableCell>{row.stimmkreisid}</TableCell>
                            <TableCell>{row.distance}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Q6 = () => {
    const [backendData, setBackendData] = useState<BackendResponse[]>([]);
    const [selectedId, setSelectedId] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q6')
            .then(response => response.json())
            .then(data => setBackendData(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);
    const ids = Array.from(new Set(backendData.map(row => row.kurzbezeichnung)));
    const handleSelectionChange = (event: SelectChangeEvent<string>) => {
        const newSelectedProductId = event.target.value as string;
        setSelectedId(newSelectedProductId);
    };
    const filteredData = backendData.filter(row => row.kurzbezeichnung === selectedId)

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
                        Partei wählen
                    </MenuItem>
                    {ids.map(id => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            {filteredData && filteredData[0] && filteredData[0].winner_or_loser !== undefined &&
                <> <a
                    style={{fontSize: 'smaller'}}>{filteredData[0].kurzbezeichnung}: {filteredData[0].winner_or_loser}</a>
                    <br/></>
            }

            <ProductTable filteredData={filteredData}/>
        </div>
    );
};

export default Q6;
