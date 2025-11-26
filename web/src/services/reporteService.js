import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useReporteService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRequest = useCallback(async (endpoint) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/reportes/${endpoint}`);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.message || err.message || 'Error al obtener los datos del reporte';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getVentasMensuales = useCallback(() => handleRequest('ventas/mensuales'), [handleRequest]);
  const getProductosMasVendidos = useCallback(() => handleRequest('productos/mas-vendidos'), [handleRequest]);
  const getReservasPorDia = useCallback(() => handleRequest('reservas/por-dia'), [handleRequest]);
  const getMediosPago = useCallback(() => handleRequest('medios-pago'), [handleRequest]);
  const getUsoSectores = useCallback(() => handleRequest('sectores/uso'), [handleRequest]);
  const getFacturacionMozos = useCallback(() => handleRequest('mozos/facturacion'), [handleRequest]);

  return {
    getVentasMensuales,
    getProductosMasVendidos,
    getReservasPorDia,
    getMediosPago,
    getUsoSectores,
    getFacturacionMozos,
    loading,
    error,
  };
};
