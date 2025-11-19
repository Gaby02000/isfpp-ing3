import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useMedioPagoService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const getMedioPagos = useCallback(async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.estado) params.append('estado', filters.estado);
      if (filters.page) params.append('page', filters.page);
      if (filters.per_page) params.append('per_page', filters.per_page);

      const response = await axios.get(`${BACKEND_URL}/api/medio-pagos/?${params.toString()}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener los medios de pago';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getMedioPago = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/medio-pagos/${id}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener el medio de pago';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const createMedioPago = useCallback(async (medioPagoData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/api/medio-pagos/`, medioPagoData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al crear el medio de pago';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateMedioPago = useCallback(async (id, medioPagoData) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/api/medio-pagos/${id}`, medioPagoData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al actualizar el medio de pago';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteMedioPago = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/api/medio-pagos/${id}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al dar de baja el medio de pago';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getTodosMedioPagos = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/medio-pagos`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener todos los medios de pago';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    getMedioPagos,
    getMedioPago,
    createMedioPago,
    updateMedioPago,
    deleteMedioPago,
    getTodosMedioPagos,
    error,
    loading
  };
};
