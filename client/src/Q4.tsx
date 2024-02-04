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
    erststimmen_stimmkreissieger: string;
    zweitstimmen_stimmkreissieger: string;
}

interface ProductTableProps {
    filteredData: BackendResponse[];
}

const ProductTable: React.FC<ProductTableProps> = ({filteredData}) => {
    return (
        <TableContainer component={Paper}>
            <Table sx={{minWidth: 650}} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Stimmkreis ID</TableCell>
                        <TableCell>erststimmen Stimmkreissieger</TableCell>
                        <TableCell>zweitstimmen Stimmkreissieger</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredData.map((row) => (
                        <TableRow
                            key={row.stimmkreisid}
                            sx={{'&:last-child td, &:last-child th': {border: 0}}}
                        >
                            <TableCell component="th" scope="row">
                                {row.stimmkreisid}
                            </TableCell>
                            <TableCell>{row.erststimmen_stimmkreissieger}</TableCell>
                            <TableCell>{row.zweitstimmen_stimmkreissieger}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Q4 = () => {
    const [backendData, setBackendData] = useState<BackendResponse[]>([]);
    const [selectedId, setSelectedId] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q4')
            .then(response => response.json())
            .then(data => setBackendData(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    const ids = Array.from(new Set(backendData.map(row => row.stimmkreisid)));

    const handleSelectionChange = (event: SelectChangeEvent<string>) => {
        setSelectedId(event.target.value as string);
    };

    const filteredData = backendData
        .filter(row => row.stimmkreisid === selectedId);
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
            <ProductTable filteredData={filteredData}/>
        </div>
    );
};

export default Q4;
