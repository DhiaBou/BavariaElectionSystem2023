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
}

interface ProductTableProps {
    filteredTimestamps: Product[]; // Assuming 'Product' is your data type
}

const ProductTable: React.FC<ProductTableProps> = ({ filteredTimestamps }) => {
    return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Stimmkreis ID</TableCell>
            <TableCell>Partei Name</TableCell>
            <TableCell>Wahlbeteiligung</TableCell>
            <TableCell>Gesamt Stimmen</TableCell>
            <TableCell>Percentage</TableCell>
            <TableCell>Gewählte Kandidaten</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {filteredTimestamps.map((product) => (
            <TableRow
              key={product.stimmkreisid}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {product.stimmkreisid}
              </TableCell>
              <TableCell>{product.parteiname}</TableCell>
              <TableCell>{product.wahlbeteiligung}</TableCell>
              <TableCell>{product.gesamt_stimmen}</TableCell>
              <TableCell>{product.percentage}</TableCell>
              <TableCell>{product.gewaehlte_kandidaten}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};



const ProductList = () => {
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
        setSelectedProductId(event.target.value as string);
    };

    // Filter timestamps for selected product ID
const filteredTimestamps = products
  .filter(product => product.stimmkreisid === selectedProductId)
  .sort((a, b) => b.gesamt_stimmen - a.gesamt_stimmen);

    return (
        <div>
            <FormControl fullWidth>
                <Select
                    value={selectedProductId}
                    onChange={handleSelectionChange}
                    displayEmpty
                    inputProps={{ 'aria-label': 'Without label' }}
                >
                    <MenuItem value="" disabled>
                        Select a Product ID
                    </MenuItem>
                    {productIds.map(id => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                    ))}
                </Select>
            </FormControl>
            <ProductTable filteredTimestamps={filteredTimestamps}/>
        </div>
    );
};

export default ProductList;
