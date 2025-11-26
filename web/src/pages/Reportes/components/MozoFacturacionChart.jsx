import React from 'react';
import { Bar } from 'react-chartjs-2';

const MozoFacturacionChart = ({ data }) => {
  const chartData = {
    labels: data.map(f => f.mozo),
    datasets: [
      {
        label: 'Facturación ($)',
        data: data.map(f => f.facturado),
        backgroundColor: 'rgba(153, 102, 255, 0.6)'
      }
    ]
  };

  return <Bar data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />;
};

export default MozoFacturacionChart;
