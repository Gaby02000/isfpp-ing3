import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useMesaService } from '../../services/mesaService';
import { useSectorService } from '../../services/sectorService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosMesas from './components/FiltrosMesas';
import TablaMesas from './components/TablaMesas';
import ModalMesa from './components/ModalMesa';
import ModalBajaMesa from './components/ModalBajaMesa';

const Mesas = () => {
  const { getMesas, createMesa, updateMesa, deleteMesa, loading } = useMesaService();
  const { getSectores } = useSectorService();
  const [mesas, setMesas] = useState([]);
  const [sectores, setSectores] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingMesa, setEditingMesa] = useState(null);
  const [deletingMesa, setDeletingMesa] = useState(null);
  const [alert, setAlert] = useState(null);
  
  // Filtros y búsqueda
  const [filtros, setFiltros] = useState({
    numero: '',
    sector_id: '',
    tipo: '',
    estado: ''
  });
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    loadMesas();
    loadSectores();
  }, []);

  const loadMesas = async (filters = {}) => {
    try {
      const response = await getMesas(filters);
      setMesas(response.data || []);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const loadSectores = async () => {
    try {
      const response = await getSectores();
      setSectores(response.data || []);
    } catch (error) {
      console.error('Error al cargar sectores:', error);
    }
  };

  // Filtrar mesas localmente y por búsqueda
  const mesasFiltradas = useMemo(() => {
    let filtered = [...mesas];

    // Búsqueda por texto (número, tipo)
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(mesa => 
        mesa.numero.toString().includes(searchLower) ||
        mesa.tipo.toLowerCase().includes(searchLower)
      );
    }

    // Filtros
    if (filtros.numero) {
      filtered = filtered.filter(mesa => 
        mesa.numero.toString() === filtros.numero
      );
    }
    if (filtros.sector_id) {
      filtered = filtered.filter(mesa => 
        mesa.id_sector.toString() === filtros.sector_id
      );
    }
    if (filtros.tipo) {
      filtered = filtered.filter(mesa => 
        mesa.tipo.toLowerCase() === filtros.tipo.toLowerCase()
      );
    }
    if (filtros.estado) {
      const mostrarBaja = filtros.estado === 'baja';
      filtered = filtered.filter(mesa => mesa.baja === mostrarBaja);
    }

    return filtered;
  }, [mesas, filtros, busqueda]);

  const handleCreate = () => {
    setEditingMesa(null);
    setShowModal(true);
  };

  const handleEdit = (mesa) => {
    setEditingMesa(mesa);
    setShowModal(true);
  };

  const handleDelete = (mesa) => {
    setDeletingMesa(mesa);
    setShowDeleteModal(true);
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      if (editingMesa) {
        await updateMesa(editingMesa.id_mesa, values);
        setAlert({ variant: 'success', message: 'Mesa modificada exitosamente' });
      } else {
        await createMesa(values);
        setAlert({ variant: 'success', message: 'Mesa creada exitosamente' });
      }
      setShowModal(false);
      resetForm();
      loadMesas();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteMesa(deletingMesa.id_mesa);
      setAlert({ variant: 'success', message: 'Mesa dada de baja exitosamente' });
      setShowDeleteModal(false);
      setDeletingMesa(null);
      loadMesas();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const handleFiltroChange = (campo, valor) => {
    setFiltros(prev => ({ ...prev, [campo]: valor || '' }));
  };

  const handleLimpiarFiltros = () => {
    setFiltros({
      numero: '',
      sector_id: '',
      tipo: '',
      estado: ''
    });
    setBusqueda('');
  };

  if (loading && mesas.length === 0) {
    return <Cargador />;
  }

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Gestión de Mesas" 
        backPath="/gestion" 
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)}>
          {alert.message}
        </Alert>
      )}

      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Listado de Mesas</h2>
        <Button variant="primary" onClick={handleCreate}>
          + Nueva Mesa
        </Button>
      </div>

      <FiltrosMesas
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        busqueda={busqueda}
        onBusquedaChange={setBusqueda}
        onLimpiar={handleLimpiarFiltros}
        sectores={sectores}
        totalMesas={mesas.length}
        mesasFiltradas={mesasFiltradas.length}
      />

      <TablaMesas
        mesas={mesasFiltradas}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <ModalMesa
        show={showModal}
        onHide={() => setShowModal(false)}
        editingMesa={editingMesa}
        onSubmit={handleSubmit}
        sectores={sectores}
      />

      <ModalBajaMesa
        show={showDeleteModal}
        onHide={() => setShowDeleteModal(false)}
        mesa={deletingMesa}
        onConfirm={handleConfirmDelete}
      />
    </Container>
  );
};

export default Mesas;
