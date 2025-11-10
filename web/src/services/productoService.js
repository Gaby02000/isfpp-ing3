import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useProductoService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const getProductos = useCallback(async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.activos) params.append('activos', filters.activos);
      if (filters.ordenar_por) params.append('ordenar_por', filters.ordenar_por);
      if (filters.page) params.append('page', filters.page);
      if (filters.per_page) params.append('per_page', filters.per_page);
      if (filters.seccion_id) params.append('seccion_id', filters.seccion_id);

      const response = await axios.get(`${BACKEND_URL}/api/productos/?${params.toString()}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener los productos';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getProducto = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/productos/${id}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener el producto';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const createProducto = useCallback(async (productoData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/api/productos/`, productoData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al crear el producto';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateProducto = useCallback(async (id, productoData) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/api/productos/${id}`, productoData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al actualizar el producto';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteProducto = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/api/productos/${id}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al dar de baja el producto';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    getProductos,
    getProducto,
    createProducto,
    updateProducto,
    deleteProducto,
    error,
    loading
  };
};
