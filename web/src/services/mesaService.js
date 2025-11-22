import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useMesaService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const getMesas = useCallback(async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.sector_id) params.append('sector_id', filters.sector_id);
      if (filters.tipo) params.append('tipo', filters.tipo);
      if (filters.estado) params.append('estado', filters.estado);
      if (filters.ordenar_por) params.append('ordenar_por', filters.ordenar_por);
      
      // Parámetros de paginación
      if (filters.page) params.append('page', filters.page);
      if (filters.per_page) params.append('per_page', filters.per_page);
      
      const response = await axios.get(`${BACKEND_URL}/api/mesas/?${params.toString()}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener las mesas';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getTiposMesas = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/mesas/tipos`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener los tipos de mesas';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getMesasDisponibles = useCallback(async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.cant_comensales) params.append('cant_comensales', filters.cant_comensales);
      if (filters.sector_id) params.append('sector_id', filters.sector_id);
      
      const response = await axios.get(`${BACKEND_URL}/api/mesas/disponibles?${params.toString()}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al obtener las mesas disponibles');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const getMesa = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/mesas/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al obtener la mesa');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);


  const createMesa = useCallback(async (mesaData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/api/mesas/`, mesaData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al crear la mesa';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateMesa = useCallback(async (id, mesaData) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/api/mesas/${id}`, mesaData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al actualizar la mesa');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteMesa = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/api/mesas/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al dar de baja la mesa');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    getMesas,
    getTiposMesas,
    getMesasDisponibles,
    getMesa,
    createMesa,
    updateMesa,
    deleteMesa,
    error,
    loading
  };
};