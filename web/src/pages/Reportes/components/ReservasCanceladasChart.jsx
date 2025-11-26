import React from 'react';
import { Line } from 'react-chartjs-2';

const ReservasCanceladasChart = ({ data }) => {
  const chartData = {
    labels: data.map(r => r.fecha),
    datasets: [
      {
        label: 'Reservas Canceladas',
        data: data.map(r => r.cantidad_cancelada),
        borderColor: 'rgba(255, 99, 132, 0.8)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.3
      }
    ]
  };

  return <Line data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />;
};

export default ReservasCanceladasChart;
