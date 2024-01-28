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
    WahlkreisId: string;
    parteiname: string;
    anzahl_ueberhangsmandate: string;
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
            <TableCell>Wahlkreis Id</TableCell>
            <TableCell>parteiname</TableCell>
            <TableCell>Anzahl Ueberhangsmandate</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {filteredTimestamps.map((product) => (
            <TableRow
              key={product.WahlkreisId}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {product.WahlkreisId}
              </TableCell>
              <TableCell component="th" scope="row">
                {product.parteiname}
              </TableCell>
              <TableCell>{product.anzahl_ueberhangsmandate}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};



const Vergleich = () => {
    const [products, setProducts] = useState<Product[]>([]);

    // Fetch data from the server
    useEffect(() => {
        fetch('http://localhost:8000/vergleich')
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

export default Vergleich;
