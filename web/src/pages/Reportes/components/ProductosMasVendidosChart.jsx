import React from 'react';
import { Bar } from 'react-chartjs-2';

const ProductosMasVendidosChart = ({ data }) => {
  const chartData = {
    labels: data.map(p => p.producto),
    datasets: [
      {
        label: 'Cantidad Vendida',
        data: data.map(p => p.cantidad),
        backgroundColor: 'rgba(255, 159, 64, 0.6)'
      }
    ]
  };

  return <Bar data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />;
};

export default ProductosMasVendidosChart;
