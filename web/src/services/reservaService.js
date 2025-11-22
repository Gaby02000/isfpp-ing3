import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useReservaService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Listar reservas con filtros y paginación
  const getReservas = useCallback(async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.cancelado) params.append('cancelado', filters.cancelado); // activo/cancelado
      if (filters.cliente_id) params.append('cliente_id', filters.cliente_id);
      if (filters.fecha_desde) params.append('fecha_desde', filters.fecha_desde);
      if (filters.fecha_hasta) params.append('fecha_hasta', filters.fecha_hasta);
      if (filters.order_by) params.append('order_by', filters.order_by);
      if (filters.page) params.append('page', filters.page);
      if (filters.per_page) params.append('per_page', filters.per_page);

      const response = await axios.get(`${BACKEND_URL}/api/reservas/?${params.toString()}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener las reservas';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  // Obtener una reserva por ID
  const getReserva = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/reservas/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al obtener la reserva');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  // Crear una nueva reserva
  const createReserva = useCallback(async (reservaData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/api/reservas/`, reservaData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al crear la reserva';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  // Actualizar una reserva existente
  const updateReserva = useCallback(async (id, reservaData) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/api/reservas/${id}`, reservaData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al actualizar la reserva');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  // Cancelar una reserva (PUT /cancelar)
  const cancelarReserva = useCallback(async (id, body = {}) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/api/reservas/${id}/cancelar`, body);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al cancelar la reserva');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  // Eliminar una reserva (si tu backend lo soporta)
  const deleteReserva = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/api/reservas/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al eliminar la reserva');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    getReservas,
    getReserva,
    createReserva,
    updateReserva,
    cancelarReserva,
    deleteReserva,
    error,
    loading
  };
};