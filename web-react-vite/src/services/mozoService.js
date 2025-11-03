import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5001';

export const useMozoService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const createMozo = useCallback(async (mozoData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/mozos`, mozoData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al crear el mozo');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const getMozos = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/mozos`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al obtener los mozos');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteMozo = useCallback(async (dni) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/mozos/${dni}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al eliminar el mozo');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateMozo = useCallback(async (dni, mozoData) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/mozos/${dni}`, mozoData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al actualizar el mozo');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    createMozo,
    getMozos,
    deleteMozo,
    updateMozo,
    error,
    loading
  };
};