import React from 'react';
import { Pie } from 'react-chartjs-2';

const PagosPorMedioChart = ({ data }) => {
  const chartData = {
    labels: data.map(m => m.medio_pago),
    datasets: [
      {
        label: 'Total Pagado',
        data: data.map(m => m.total),
        backgroundColor: [
          '#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'
        ]
      }
    ]
  };

  return <Pie data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />;
};

export default PagosPorMedioChart;
