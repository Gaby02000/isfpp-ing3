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
import Paginacion from '../../components/common/Paginacion';

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
  
  // Paginación
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 1,
    has_next: false,
    has_prev: false
  });
  
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

  useEffect(() => {
    // Recargar cuando cambian los filtros o la página
    loadMesas();
  }, [pagination.page, filtros.sector_id, filtros.tipo, filtros.estado]);

  const loadMesas = async (page = pagination.page) => {
    try {
      const filters = {
        page,
        per_page: pagination.per_page,
        sector_id: filtros.sector_id || undefined,
        tipo: filtros.tipo || undefined,
        estado: filtros.estado || undefined
      };
      
      const response = await getMesas(filters);
      
      // Aplicar búsqueda local si hay texto de búsqueda
      let mesasData = response.data || [];
      if (busqueda) {
        const searchLower = busqueda.toLowerCase();
        mesasData = mesasData.filter(mesa => 
          mesa.numero.toString().includes(searchLower) ||
          mesa.tipo.toLowerCase().includes(searchLower)
        );
      }
      
      setMesas(mesasData);
      
      // Actualizar información de paginación
      if (response.pagination) {
        setPagination(response.pagination);
      }
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

  // Filtrar mesas localmente solo por búsqueda (filtros ya vienen del backend)
  const mesasFiltradas = useMemo(() => {
    let filtered = [...mesas];

    // Solo búsqueda local (filtros van al backend)
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(mesa => 
        mesa.numero.toString().includes(searchLower) ||
        mesa.tipo.toLowerCase().includes(searchLower)
      );
    }

    return filtered;
  }, [mesas, busqueda]);

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
    // Resetear a página 1 cuando cambian los filtros
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handleLimpiarFiltros = () => {
    setFiltros({
      numero: '',
      sector_id: '',
      tipo: '',
      estado: ''
    });
    setBusqueda('');
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
    loadMesas(page);
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
        totalMesas={pagination.total}
        mesasFiltradas={mesasFiltradas.length}
      />

      <TablaMesas
        mesas={mesasFiltradas}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <Paginacion
        currentPage={pagination.page}
        totalPages={pagination.total_pages}
        hasNext={pagination.has_next}
        hasPrev={pagination.has_prev}
        onPageChange={handlePageChange}
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
