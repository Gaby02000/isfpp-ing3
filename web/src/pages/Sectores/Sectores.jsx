import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useSectorService } from '../../services/sectorService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosSectores from './components/FiltrosSectores';
import TablaSectores from './components/TablaSectores';
import ModalSector from './components/ModalSector';
import ModalBajaSector from './components/ModalBajaSector';
import Paginacion from '../../components/common/Paginacion';

const Sectores = () => {
  const { getSectores, createSector, updateSector, deleteSector, loading } = useSectorService();
  const [sectores, setSectores] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingSector, setEditingSector] = useState(null);
  const [deletingSector, setDeletingSector] = useState(null);
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
    estado: ''
  });
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    loadSectores();
  }, []);

  useEffect(() => {
    // Recargar cuando cambian los filtros o la página
    loadSectores();
  }, [pagination.page, filtros.estado]);

  const loadSectores = async (page = pagination.page) => {
    try {
      const filters = {
        page,
        per_page: pagination.per_page,
        estado: filtros.estado || undefined
      };
      
      const response = await getSectores(filters);
      
      // Aplicar búsqueda local si hay texto de búsqueda
      let sectoresData = response.data || [];
      if (busqueda) {
        const searchLower = busqueda.toLowerCase();
        sectoresData = sectoresData.filter(sector => 
          sector.numero.toString().includes(searchLower)
        );
      }
      
      setSectores(sectoresData);
      
      // Actualizar información de paginación
      if (response.pagination) {
        setPagination(response.pagination);
      }
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message || 'Error al cargar sectores' });
    }
  };

  // Filtrar sectores localmente solo por búsqueda (filtros ya vienen del backend)
  const sectoresFiltrados = useMemo(() => {
    let filtered = [...sectores];

    // Solo búsqueda local (filtros van al backend)
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(sector => 
        sector.numero.toString().includes(searchLower)
      );
    }

    return filtered;
  }, [sectores, busqueda]);

  const handleCreate = () => {
    setEditingSector(null);
    setShowModal(true);
  };

  const handleEdit = (sector) => {
    setEditingSector(sector);
    setShowModal(true);
  };

  const handleDelete = (sector) => {
    setDeletingSector(sector);
    setShowDeleteModal(true);
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      if (editingSector) {
        await updateSector(editingSector.id_sector, values);
        setAlert({ variant: 'success', message: 'Sector modificado exitosamente' });
      } else {
        await createSector(values);
        setAlert({ variant: 'success', message: 'Sector creado exitosamente' });
      }
      setShowModal(false);
      resetForm();
      loadSectores();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteSector(deletingSector.id_sector);
      setAlert({ variant: 'success', message: 'Sector dado de baja exitosamente' });
      setShowDeleteModal(false);
      setDeletingSector(null);
      loadSectores();
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
      estado: ''
    });
    setBusqueda('');
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
    loadSectores(page);
  };

  if (loading && sectores.length === 0) {
    return <Cargador />;
  }

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Gestión de Sectores" 
        backPath="/gestion" 
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)}>
          {alert.message}
        </Alert>
      )}

      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Listado de Sectores</h2>
        <Button variant="primary" onClick={handleCreate}>
          + Nuevo Sector
        </Button>
      </div>

      <FiltrosSectores
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        busqueda={busqueda}
        onBusquedaChange={setBusqueda}
        onLimpiar={handleLimpiarFiltros}
        totalSectores={pagination.total}
        sectoresFiltrados={sectoresFiltrados.length}
      />

      <TablaSectores
        sectores={sectoresFiltrados}
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

      <ModalSector
        show={showModal}
        onHide={() => setShowModal(false)}
        editingSector={editingSector}
        onSubmit={handleSubmit}
      />

      <ModalBajaSector
        show={showDeleteModal}
        onHide={() => setShowDeleteModal(false)}
        sector={deletingSector}
        onConfirm={handleConfirmDelete}
      />
    </Container>
  );
};

export default Sectores;
