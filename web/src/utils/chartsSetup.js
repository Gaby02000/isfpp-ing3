// src/utils/chartsSetup.js

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

// Registrar escalas, elementos y plugins globalmente
ChartJS.register(
  CategoryScale, // Para ejes tipo 'category'
  LinearScale,   // Para ejes numéricos
  BarElement,    // Para gráficos de barras
  PointElement,  // Para gráficos de línea/puntos
  LineElement,   // Para gráficos de línea
  ArcElement,    // Para gráficos de pastel/doughnut
  Title,         // Título del chart
  Tooltip,       // Tooltip al pasar el mouse
  Legend,        // Leyenda
  Filler         // Para rellenar áreas en line charts
);

// Opcional: puedes agregar configuraciones globales por defecto
ChartJS.defaults.font.family = 'Arial, sans-serif';
ChartJS.defaults.plugins.legend.position = 'top';
ChartJS.defaults.plugins.tooltip.enabled = true;
