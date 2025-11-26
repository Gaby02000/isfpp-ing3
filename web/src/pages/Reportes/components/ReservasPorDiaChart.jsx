import React from 'react';
import { Line } from 'react-chartjs-2';

const ReservasPorDiaChart = ({ data }) => {
  const chartData = {
    labels: data.map(r => r.fecha),
    datasets: [
      {
        label: 'Reservas por Día',
        data: data.map(r => r.cantidad),
        borderColor: 'rgba(54, 162, 235, 0.8)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.3
      }
    ]
  };

  return <Line data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />;
};

export default ReservasPorDiaChart;
