import React from 'react';
import { Bar } from 'react-chartjs-2';

const VentasMensualesChart = ({ data }) => {
  const chartData = {
    labels: data.map(v => v.mes),
    datasets: [
      {
        label: 'Ventas ($)',
        data: data.map(v => v.total),
        backgroundColor: 'rgba(75, 192, 192, 0.6)'
      }
    ]
  };

  return <Bar data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />;
};

export default VentasMensualesChart;
