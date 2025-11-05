import { useState, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';

export const useSectorService = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const getSectores = useCallback(async (estado = null) => {
    try {
      setLoading(true);
      const params = estado ? `?estado=${estado}` : '';
      const response = await axios.get(`${BACKEND_URL}/api/sectores${params}`);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al obtener los sectores';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getSector = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/sectores/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al obtener el sector');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const createSector = useCallback(async (sectorData) => {
    try {
      setLoading(true);
      const response = await axios.post(`${BACKEND_URL}/api/sectores/`, sectorData);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error al crear el sector';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateSector = useCallback(async (id, sectorData) => {
    try {
      setLoading(true);
      const response = await axios.put(`${BACKEND_URL}/api/sectores/${id}`, sectorData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al actualizar el sector');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteSector = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${BACKEND_URL}/api/sectores/${id}`);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.message || 'Error al dar de baja el sector');
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    getSectores,
    getSector,
    createSector,
    updateSector,
    deleteSector,
    error,
    loading
  };
};

