import React, {useEffect, useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {FormControl, MenuItem, Select, SelectChangeEvent} from "@mui/material";

interface Product {
    kurzbezeichnung: string;
    name: string;
    stimmkreisid: string;
    distance: number;
    rn: number;
    winner_or_loser: string;
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
                        <TableCell>Partei</TableCell>
                        <TableCell>Kandidatenname</TableCell>
                        <TableCell>Stimmkreis</TableCell>
                        <TableCell>Distanz zum nächsten oder zum ersten</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredTimestamps.map((product) => (
                        <TableRow
                            sx={{'&:last-child td, &:last-child th': {border: 0}}}
                        >
                            <TableCell component="th" scope="row">
                                {product.kurzbezeichnung}
                            </TableCell>
                            <TableCell component="th" scope="row">
                                {product.name}
                            </TableCell>
                            <TableCell>{product.stimmkreisid}</TableCell>
                            <TableCell>{product.distance}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Q6 = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [selectedProductId, setSelectedProductId] = useState('');

    // Fetch data from the server
    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q6')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);
    const productIds = Array.from(new Set(products.map(product => product.kurzbezeichnung)));
    const handleSelectionChange = (event: SelectChangeEvent<string>) => {
        const newSelectedProductId = event.target.value as string;
        setSelectedProductId(newSelectedProductId);
    };
    const filteredTimestamps = products.filter(product => product.kurzbezeichnung === selectedProductId)

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
                        Partei wählen
                    </MenuItem>
                    {productIds.map(id => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            {filteredTimestamps && filteredTimestamps[0] && filteredTimestamps[0].winner_or_loser !== undefined &&
                <> <a
                    style={{fontSize: 'smaller'}}>{filteredTimestamps[0].kurzbezeichnung}: {filteredTimestamps[0].winner_or_loser}</a>
                    <br/></>
            }

            <ProductTable filteredTimestamps={filteredTimestamps}/>
        </div>
    );
};

export default Q6;
