import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useComandaService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

    const getComandas = useCallback(async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
        if (filters.fecha) params.append('fecha', filters.fecha);
        if (filters.id_mesa) params.append('id_mesa', filters.id_mesa);
        if (filters.id_mozo) params.append('id_mozo', filters.id_mozo);
        if (filters.estado) params.append('estado', filters.estado);
        if (filters.ordenar_por) params.append('ordenar_por', filters.ordenar_por);

        // Parámetros de paginación
        if (filters.page) params.append('page', filters.page);
        if (filters.per_page) params.append('per_page', filters.per_page);

        const response = await axios.get(`${BACKEND_URL}/api/comandas/?${params.toString()}`);
        return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener las comandas';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
    }, []);

const getComanda = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/comandas/${id}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener la comanda';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }   
    }, []);

const createComanda = useCallback(async (comandaData) => {
    try {
      setLoading(true); 
        const response = await axios.post(`${BACKEND_URL}/api/comandas/`, comandaData);
        return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al crear la comanda';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
    }, []);

const updateComanda = useCallback(async (id, comandaData) => {
    try {
      setLoading(true);
        const response = await axios.put(`${BACKEND_URL}/api/comandas/${id}`, comandaData);
        return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al actualizar la comanda';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
    finally {
      setLoading(false);
    }
    }, []);
const deleteComanda = useCallback(async (id) => {
    try {
      setLoading(true);
        const response = await axios.delete(`${BACKEND_URL}/api/comandas/${id}`);
        return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al dar de baja la comanda';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
    }, []);

  return {
    getComandas,
    getComanda,
    createComanda,
    updateComanda,
    deleteComanda,
    loading,
    error,
  };
}