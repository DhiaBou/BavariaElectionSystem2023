import React, {useEffect, useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


const TableComponent: React.FC<any> = ({filteredData}) => {
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
                        filteredData.map((row) => (
                            <TableRow
                                key={row.parteiid}
                                sx={{'&:last-child td, &:last-child th': {border: 0}}}
                            >
                                <TableCell>{row.parteiname}</TableCell>
                                <TableCell>{row.erstimmen2018}</TableCell>
                                <TableCell>{row.zweitstimmen2018}</TableCell>
                                <TableCell>{row.gesammtstimmen2018}</TableCell>
                                <TableCell>{row.erststimmen}</TableCell>
                                <TableCell>{row.zweitestimmen}</TableCell>
                                <TableCell>{row.gesamt_stimmen}</TableCell>
                                <TableCell>{row.vote_percentage}</TableCell>
                                <TableCell>{row.difference_gesamt_stimmen}</TableCell>
                                <TableCell>{row.anzahl_sitze}</TableCell>
                                <TableCell>{row.difference_anzahl_sitze}</TableCell>
                            </TableRow>
                        ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};


const Vergleich = () => {
    const [backendData, setBackendData] = useState<any[]>([]);

    // Fetch data from the server
    useEffect(() => {
        fetch('http://localhost:8000/vergleich')
            .then(response => response.json())
            .then(data => setBackendData(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);

    return (
        <div>
            <TableComponent filteredData={backendData}/>
        </div>
    );
};

export default Vergleich;
