import React, {useEffect, useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

interface Product {
    kurzbezeichnung: string;
    kandidate_name: string;
    stimmkreis_name: string;
    distance: number;
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
                        <TableCell>Distanz zum nächsten</TableCell>
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
                                {product.kandidate_name}
                            </TableCell>
                            <TableCell>{product.stimmkreis_name}</TableCell>
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

    // Fetch data from the server
    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q6')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    return (
        <div>
            <ProductTable filteredTimestamps={products}/>
        </div>
    );
};

export default Q6;
