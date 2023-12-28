import { Grid } from '@mui/material';
import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
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

const MyPieChart = () => {
    // Explicitly type the initial state
    const [chartData, setChartData] = useState<ChartData>({
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                // ... other colors
            ]
        }]
    });

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/q1')
            .then(response => response.json())
            .then((data: DataItem[]) => {
                const labels = data.map((item: DataItem) => `${item.kurzbezeichnung}: ${item.count}`);
                const counts = data.map((item: DataItem) => item.count);

                setChartData(prevChartData => ({
                    ...prevChartData,
                    labels: labels,
                    datasets: [{
                        ...prevChartData.datasets[0],
                        data: counts
                    }]
                }));
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, []);
    return (
            <Grid container spacing={2} justifyContent="center" alignItems="center">
      <Grid item xs={4} style={{ display: 'flex', justifyContent: 'center' }}>
        <Pie data={chartData} width={100} height={100} />
      </Grid>
    </Grid>
    );
}

export default MyPieChart;


