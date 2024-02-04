import React, {useEffect, useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

interface BackendResponse {
    WahlkreisId: string;
    parteiname: string;
    anzahl_ueberhangsmandate: string;
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
                        <TableCell>Wahlkreis Id</TableCell>
                        <TableCell>parteiname</TableCell>
                        <TableCell>Anzahl Ueberhangsmandate</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredData.map((row) => (
                        <TableRow
                            key={row.WahlkreisId}
                            sx={{'&:last-child td, &:last-child th': {border: 0}}}
                        >
                            <TableCell component="th" scope="row">
                                {row.WahlkreisId}
                            </TableCell>
                            <TableCell component="th" scope="row">
                                {row.parteiname}
                            </TableCell>
                            <TableCell>{row.anzahl_ueberhangsmandate}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Q5 = () => {
    const [backendData, setBackendData] = useState<BackendResponse[]>([]);

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q5')
            .then(response => response.json())
            .then(data => setBackendData(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    return (
        <div>
            <ProductTable filteredData={backendData}/>
        </div>
    );
};

export default Q5;
