import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useFacturaService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

 const getFacturas = useCallback(async (filters = {}) => {
  console.log('🔷 [getFacturas] Filtros recibidos:', filters);
  
  try {
    setLoading(true);
    const params = new URLSearchParams();
    
    if (filters.page) params.append('page', filters.page);
    if (filters.per_page) params.append('per_page', filters.per_page);
    if (filters.id_comanda) params.append('id_comanda', filters.id_comanda);
    if (filters.solo_impagas) params.append('solo_impagas', 'true');
    
    const url = `${BACKEND_URL}/api/facturas/?${params.toString()}`;
    console.log('🔷 [getFacturas] URL:', url);
    
    const response = await axios.get(url);
    console.log('🔷 [getFacturas] Respuesta:', response.data);
    
    return response.data;
  } catch (error) {
    console.error('❌ [getFacturas] Error:', error);
    const errorMessage = error.response?.data?.message || error.message || 'Error al obtener las facturas';
    setError(errorMessage);
    throw new Error(errorMessage);
  } finally {
    setLoading(false);
  }
}, []);

  const getFactura = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/facturas/${id}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener la factura';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const generarFacturaDesdeComanda = useCallback(async (id_comanda, id_cliente) => {
    
    try {
      setLoading(true);
      
      const body = { id_cliente };
      
      const response = await axios.post(
        `${BACKEND_URL}/api/facturas/generar-desde-comanda/${id_comanda}`,
        body,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      console.log('✅ [Service] Respuesta exitosa:', response.data);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al generar la factura';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []); // ← IMPORTANTE: array de dependencias vacío

  const anularFactura = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/api/facturas/${id}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al anular la factura';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    getFacturas,
    getFactura,
    generarFacturaDesdeComanda,
    anularFactura,
    loading,
    error,
  };
};