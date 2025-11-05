import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useSectorService } from '../../services/sectorService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosSectores from './components/FiltrosSectores';
import TablaSectores from './components/TablaSectores';
import ModalSector from './components/ModalSector';
import ModalBajaSector from './components/ModalBajaSector';

const Sectores = () => {
  const { getSectores, createSector, updateSector, deleteSector, loading } = useSectorService();
  const [sectores, setSectores] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingSector, setEditingSector] = useState(null);
  const [deletingSector, setDeletingSector] = useState(null);
  const [alert, setAlert] = useState(null);
  
  // Filtros y búsqueda
  const [filtros, setFiltros] = useState({
    numero: '',
    estado: ''
  });
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    loadSectores();
  }, []);

  const loadSectores = async () => {
    try {
      const response = await getSectores();
      setSectores(response.data || []);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  // Filtrar sectores localmente y por búsqueda
  const sectoresFiltrados = useMemo(() => {
    let filtered = [...sectores];

    // Búsqueda por texto (número)
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(sector => 
        sector.numero.toString().includes(searchLower)
      );
    }

    // Filtros
    if (filtros.numero) {
      filtered = filtered.filter(sector => 
        sector.numero.toString() === filtros.numero
      );
    }
    if (filtros.estado) {
      const mostrarBaja = filtros.estado === 'baja';
      filtered = filtered.filter(sector => sector.baja === mostrarBaja);
    }

    return filtered;
  }, [sectores, filtros, busqueda]);

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
  };

  const handleLimpiarFiltros = () => {
    setFiltros({
      numero: '',
      estado: ''
    });
    setBusqueda('');
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
        totalSectores={sectores.length}
        sectoresFiltrados={sectoresFiltrados.length}
      />

      <TablaSectores
        sectores={sectoresFiltrados}
        onEdit={handleEdit}
        onDelete={handleDelete}
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
