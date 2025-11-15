import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:99';

export const useClienteService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const getClientes = useCallback(async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.documento) params.append('documento', filters.documento);
      if (filters.nombre) params.append('nombre', filters.nombre);
      if (filters.apellido) params.append('apellido', filters.apellido);
      if (filters.ordenar_por) params.append('ordenar_por', filters.ordenar_por);
      
      // Parámetros de paginación
      if (filters.page) params.append('page', filters.page);
      if (filters.per_page) params.append('per_page', filters.per_page);
      
      const response = await axios.get(`${BACKEND_URL}/api/clientes/?${params.toString()}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener los clientes';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);



  const getCliente = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/clientes/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al obtener el cliente');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const createCliente = useCallback(async (clienteData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/api/clientes/`, clienteData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al crear el cliente';
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateCliente = useCallback(async (id, clienteData) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/api/clientes/${id}`, clienteData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al actualizar el cliente');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteCliente = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/api/clientes/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al dar de baja el cliente');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    getClientes,
    getCliente,
    createCliente,
    updateCliente,
    deleteCliente,
    error,
    loading
  };
};

