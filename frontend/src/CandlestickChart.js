import React, { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    TimeScale,
} from 'chart.js';
import { CandlestickController, CandlestickElement } from 'chartjs-chart-financial';
import 'chartjs-adapter-date-fns';
import { Chart } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    TimeScale,
    CandlestickController,
    CandlestickElement
);

function CandlestickChart({ symbol }) {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:5000/stocks/${symbol}`)
            .then((res) => res.json())
            .then((json) => {
                const transformed = json.map((item) => ({
                    x: new Date(item.ts).getTime(),
                    o: parseFloat(item.open),
                    h: parseFloat(item.high),
                    l: parseFloat(item.low),
                    c: parseFloat(item.price)
                }));
                setChartData(transformed);
            })
            .catch((err) => console.error(err));
    }, [symbol]);

    const data = {
        datasets: [{
            label: symbol,
            data: chartData,
            borderWidth: 2,
            borderColor: '#000',
            color: {
                // up: '#26a69a',
                down: '#ef5350',
            },
            backgroundColor: {
                up: 'rgba(38, 166, 154, 0.5)',
                down: 'rgba(239, 83, 80, 0.5)',
            }
        }]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'minute',
                    displayFormats: {
                        minute: 'h:mm'
                    }
                },
                ticks: {
                    color: 'yellow'
                },
                grid: {
                    display: true,
                    // color: 'rgba(0, 0, 0, 0.1)'
                    // color: 'yellow'
                }
            },
            y: {
                type: 'linear',
                grace: '10%',
                ticks: {
                    precision: 2,
                    color: 'yellow'
                },
                grid: {
                    display: true,
                    color: 'yellow'
                }
            }
        },
        animation: {
            duration: 0
        }
    };

    return (
        <div className="w-full h-96 p-4 border rounded-lg shadow-sm bg-black">
            <Chart
                type="candlestick"
                data={data}
                options={options}
            />
        </div>
    );
}

export default CandlestickChart;