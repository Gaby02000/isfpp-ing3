import React from 'react';
import { Pie } from 'react-chartjs-2';

const SectorUsoChart = ({ data }) => {
  const chartData = {
    labels: data.map(s => s.sector),
    datasets: [
      {
        label: 'Uso de Sectores',
        data: data.map(s => s.uso),
        backgroundColor: [
          '#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'
        ]
      }
    ]
  };

  return <Pie data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />;
};

export default SectorUsoChart;
