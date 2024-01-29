import React, {useEffect, useState} from 'react';
import {FormControl, MenuItem, Select, SelectChangeEvent} from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

interface Product {
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
    filteredTimestamps: Product[]; // Assuming 'Product' is your data type
}

const ProductTable: React.FC<ProductTableProps> = ({filteredTimestamps}) => {
    return (
        <TableContainer component={Paper}>
            <Table sx={{minWidth: 650}} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Partei Name</TableCell>
                        <TableCell>Erststimmen</TableCell>
                        <TableCell>Zweitstimmen</TableCell>
                        <TableCell>Gesamt Stimmen</TableCell>
                        <TableCell>Percentage</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {    // @ts-ignore
                        filteredTimestamps.map((product) => (
                            <TableRow
                                key={product.stimmkreisid + product.parteiname}
                                sx={{'&:last-child td, &:last-child th': {border: 0}}}
                            >
                                <TableCell>{product.parteiname}</TableCell>
                                <TableCell>{product.erststimmen}</TableCell>
                                <TableCell>{product.zweite_stimme}</TableCell>
                                <TableCell>{product.gesamt_stimmen}</TableCell>
                                <TableCell>{product.percentage}</TableCell>
                            </TableRow>
                        ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Q3 = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [selectedProductId, setSelectedProductId] = useState('');

    // Fetch data from the server
    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q3')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    // Extract distinct product IDs
    const productIds = Array.from(new Set(products.map(product => product.stimmkreisid)));

    // Handle selection change
    const handleSelectionChange = (event: SelectChangeEvent<string>) => {
        const newSelectedProductId = event.target.value as string;
        setSelectedProductId(newSelectedProductId);
    };

    const filteredTimestamps = products.filter(product => product.stimmkreisid === selectedProductId)
    return (
        <div>
            <FormControl fullWidth>
                <Select
                    value={selectedProductId}
                    onChange={handleSelectionChange}
                    displayEmpty
                    inputProps={{'aria-label': 'Without label'}}
                >
                    <MenuItem value="" disabled>
                        Stimmkreiswählen
                    </MenuItem>
                    {productIds.map(id => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            {filteredTimestamps && filteredTimestamps[0] && filteredTimestamps[0].wahlbeteiligung !== undefined &&
                <>
                    <a style={{fontSize: 'smaller'}}>Wahlbeteiligung: {filteredTimestamps[0].wahlbeteiligung}%</a> <br/>
                    <a style={{fontSize: 'smaller'}}>Gewählte
                        Kandidaten: {filteredTimestamps[0].gewaehlte_kandidaten} - {filteredTimestamps[0].parteiname}</a>                </>
            }
            <ProductTable filteredTimestamps={filteredTimestamps}/>
        </div>
    );
}
export default Q3;
