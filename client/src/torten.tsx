import {Grid} from '@mui/material';
import React, {useEffect, useState} from 'react';
import {Pie} from 'react-chartjs-2';
import 'chart.js/auto';
import TableContainer from "@mui/material/TableContainer";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import TableBody from "@mui/material/TableBody";

interface DataItem {
    kurzbezeichnung: number;
    count: number;
}

interface ProductTableProps {
    filteredData: DataItem[];
}

const TableComponent: React.FC<ProductTableProps> = ({filteredData}) => {
    return (
        <TableContainer component={Paper}>
            <Table sx={{minWidth: 400}} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Parteinamen</TableCell>
                        <TableCell>Anzahl Abgeordnete</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredData.map((row) => (
                        <TableRow
                            key={row.kurzbezeichnung}
                            sx={{'&:last-child td, &:last-child th': {border: 0}}}
                        >
                            <TableCell component="th" scope="row">
                                {row.kurzbezeichnung}
                            </TableCell>
                            <TableCell component="th" scope="row">
                                {row.count}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

interface ChartData {
    labels: string[];
    datasets: {
        data: number[];
        backgroundColor: string[];
    }[];
}

const ParlementVerteilung = () => {
    const [backendData, setBackendData] = useState<DataItem[]>([]);

    const [chartData, setChartData] = useState<ChartData>({
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: []
        }]
    });

    const partyColors = [
        'rgba(255, 193, 7, 0.6)',    // Vibrant Orange
        'rgba(76, 175, 80, 0.6)',    // Calming Green
        'rgba(156, 39, 176, 0.6)',   // Royal Purple
        'rgba(255, 87, 34, 0.6)',    // Fiery Red-Orange
        'rgba(33, 150, 243, 0.6)'    // Soothing Blue

    ];

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q1')
            .then(response => response.json())
            .then((data: DataItem[]) => {
                setBackendData(data)
                const labels = data.map(item => `${item.kurzbezeichnung}: ${item.count}`);
                const counts = data.map(item => item.count);

                setChartData(prevChartData => ({
                    ...prevChartData,
                    labels: labels,
                    datasets: [{
                        ...prevChartData.datasets[0],
                        data: counts,
                        backgroundColor: partyColors.slice(0, data.length)
                    }]
                }));
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, []);

    return (
        <Grid container spacing={2} justifyContent="center" alignItems="center" direction="row">
            <Grid item xs={4} style={{display: 'flex', justifyContent: 'center'}}>
                <Pie data={chartData} width={60} height={60}/>
            </Grid>
            <Grid item xs={4} style={{display: 'flex', justifyContent: 'center'}}>
                <TableComponent filteredData={backendData}/>
            </Grid>
        </Grid>
    );
};


export default ParlementVerteilung;