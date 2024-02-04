import React, {useEffect, useState} from 'react';
import {Bar} from 'react-chartjs-2';

// @ts-nocheck

interface Dict {
    [key: string]: {
        [key: string]: number;
    };
}

interface DiagramProps {
    data: Dict;
}

const Diagram: React.FC<DiagramProps> = ({data}) => {
    const parties = Object.values(data).flatMap(region =>
        Object.keys(region).filter(key => key !== "einkommen")
    );
    const uniqueParties = Array.from(new Set(parties)).sort();
    const partyColors = [
        'rgba(255, 193, 7, 0.6)',    // Vibrant Orange
        'rgba(76, 175, 80, 0.6)',    // Calming Green
        'rgba(156, 39, 176, 0.6)',   // Royal Purple
        'rgba(255, 87, 34, 0.6)',    // Fiery Red-Orange
        'rgba(33, 150, 243, 0.6)'    // Soothing Blue
    ];

    const datasets = uniqueParties.map((party, i) => ({
        type: 'bar',
        label: party,
        data: Object.entries(data).map(([region, values]) => values[party] || 0),
        backgroundColor: partyColors[i],
    }));

    const einkommenData = {
        type: 'line',
        label: 'Einkommen',
        data: Object.entries(data).map(([region, values]) => values.einkommen),
        borderColor: 'rgba(0, 0, 0, 0.8)',
        borderWidth: 2,
        fill: false,
        yAxisID: 'y1',
    };

    // @ts-ignore
    datasets.push(einkommenData);

    const chartData = {
        labels: Object.keys(data),
        datasets,
    };

    const options = {
        scales: {
            y: {
                beginAtZero: true,
                position: 'left',
                id: 'y',
            },
            y1: {
                beginAtZero: true,
                position: 'right',
                id: 'y1',
                grid: {
                    drawOnChartArea: false,
                },
            }
        },
        plugins: {
            legend: {
                position: 'top',
            },
        },
        responsive: true,
        maintainAspectRatio: false,
    };


    return (
        <div style={{height: "500px", width: "100%"}}>{// @ts-ignore
            <Bar data={chartData} options={options}/>}
        </div>
    );
};
const Einkommen = () => {
    const [backendData, setBackendData] = useState<any>([]);

    useEffect(() => {
        fetch('http://localhost:8000/wahlkreis/einkommen')
            .then(response => response.json())
            .then(data => setBackendData(data))
            .catch(error => console.error('There was an error fetching the data', error));
    }, []);
    return <Diagram data={backendData}/>
}

export default Einkommen
