import {Grid} from '@mui/material';
import React, {useEffect, useState} from 'react';
import {Pie} from 'react-chartjs-2';
import 'chart.js/auto';

interface DataItem {
    kurzbezeichnung: number;
    count: number;
}

// Define an interface for the chart data
interface ChartData {
    labels: string[];
    datasets: {
        data: number[];
        backgroundColor: string[];
    }[];
}

const ParlementVerteilung = () => {
    const [chartData, setChartData] = useState<ChartData>({
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: [] // Will be set dynamically
        }]
    });

    // Array of colors for each party
    const partyColors = [
        'rgba(255, 193, 7, 0.6)',    // Vibrant Orange
        'rgba(76, 175, 80, 0.6)',    // Calming Green
        'rgba(156, 39, 176, 0.6)',   // Royal Purple
        'rgba(255, 87, 34, 0.6)',    // Fiery Red-Orange
        'rgba(33, 150, 243, 0.6)'    // Soothing Blue
        // ... Add more colors for more parties
    ];

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q1')
            .then(response => response.json())
            .then((data: DataItem[]) => {
                const labels = data.map(item => `${item.kurzbezeichnung}: ${item.count}`);
                const counts = data.map(item => item.count);

                setChartData(prevChartData => ({
                    ...prevChartData,
                    labels: labels,
                    datasets: [{
                        ...prevChartData.datasets[0],
                        data: counts,
                        backgroundColor: partyColors.slice(0, data.length) // Use only as many colors as there are parties
                    }]
                }));
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, []);

    return (
        <Grid container spacing={2} justifyContent="center" alignItems="center">
            <Grid item xs={4} style={{display: 'flex', justifyContent: 'center'}}>
                <Pie data={chartData} width={80} height={80}/>
            </Grid>
        </Grid>
    );
}

export default ParlementVerteilung;