import React, {useEffect, useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


const ProductTable: React.FC<any> = ({filteredTimestamps}) => {
    // @ts-ignore
    return (
        <TableContainer component={Paper}>
            <Table sx={{minWidth: 650}} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Partei</TableCell>
                        <TableCell>Erststimmen 2018</TableCell>
                        <TableCell>Zweitstimmen 2018</TableCell>
                        <TableCell>Gesamtstimmen 2018</TableCell>
                        <TableCell>Erststimmen 2023</TableCell>
                        <TableCell>Zweitstimmen 2023</TableCell>
                        <TableCell>Gesamtstimmen 2023</TableCell>
                        <TableCell>2023 %</TableCell>
                        <TableCell>Differenz Gesammtstimmen</TableCell>
                        <TableCell>Anzahl Abgeordnete</TableCell>
                        <TableCell>Differenz Anzahl Abgeordnete</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {
                        // @ts-ignore
                        filteredTimestamps.map((product) => (
                            <TableRow
                                key={product.parteiid}
                                sx={{'&:last-child td, &:last-child th': {border: 0}}}
                            >
                                <TableCell>{product.parteiname}</TableCell>
                                <TableCell>{product.erstimmen2018}</TableCell>
                                <TableCell>{product.zweitstimmen2018}</TableCell>
                                <TableCell>{product.gesammtstimmen2018}</TableCell>
                                <TableCell>{product.erststimmen}</TableCell>
                                <TableCell>{product.zweitestimmen}</TableCell>
                                <TableCell>{product.gesamt_stimmen}</TableCell>
                                <TableCell>{product.vote_percentage}</TableCell>
                                <TableCell>{product.difference_gesamt_stimmen}</TableCell>
                                <TableCell>{product.anzahl_sitze}</TableCell>
                                <TableCell>{product.difference_anzahl_sitze}</TableCell>
                            </TableRow>
                        ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Vergleich = () => {
    const [products, setProducts] = useState<any[]>([]);

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
