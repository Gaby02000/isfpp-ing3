import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useMozoService } from '../../services/mozoService';
import { useSectorService } from '../../services/sectorService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosMozos from './components/FiltrosMozos';
import TablaMozos from './components/TablaMozos';
import ModalMozo from './components/ModalMozos';
import ModalBajaMozo from './components/ModalBajaMozo';
import Paginacion from '../../components/common/Paginacion';

const Mozos = () => {
  const { getMozos, createMozo, updateMozo, deleteMozo, loading } = useMozoService();
  const { getTodosSectores } = useSectorService();

  const [mozos, setMozos] = useState([]);
  const [sectores, setSectores] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingMozo, setEditingMozo] = useState(null);
  const [deletingMozo, setDeletingMozo] = useState(null);
  const [alert, setAlert] = useState(null);

  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 1,
    has_next: false,
    has_prev: false
  });

  const [filtros, setFiltros] = useState({
    activos: '',
    sector_id: ''
  });

  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    loadMozos();
    loadSectores();
  }, []);

  useEffect(() => {
    loadMozos();
  }, [pagination.page, filtros.activos, filtros.sector_id]);

  const loadMozos = async (page = pagination.page) => {
    try {
      const filters = {
        page,
        per_page: pagination.per_page,
        activos: filtros.activos || undefined,
        sector_id: filtros.sector_id || undefined
      };

      const response = await getMozos(filters);
      let mozosData = response.data || [];

      if (busqueda) {
        const searchLower = busqueda.toLowerCase();
        mozosData = mozosData.filter(m =>
          m.nombre_apellido.toLowerCase().includes(searchLower) ||
          m.documento.toString().includes(searchLower)
        );
      }

      setMozos(mozosData);

      if (response.pagination) {
        setPagination(response.pagination);
      }
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const loadSectores = async () => {
    try {
      const response = await getTodosSectores();
      setSectores(response.data || []);
    } catch {
      setSectores([]);
    }
  };

  const mozosFiltrados = useMemo(() => {
    let filtered = [...mozos];
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(m =>
        m.nombre_apellido.toLowerCase().includes(searchLower) ||
        m.documento.toString().includes(searchLower)
      );
    }
    return filtered;
  }, [mozos, busqueda]);

  const handleCreate = () => {
    setEditingMozo(null);
    setShowModal(true);
  };

  const handleEdit = (mozo) => {
    setEditingMozo(mozo);
    setShowModal(true);
  };

  const handleDelete = (mozo) => {
    setDeletingMozo(mozo);
    setShowDeleteModal(true);
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    console.log("handleSubmit ejecutado", values);
    try {
      const payload = {
        documento: values.documento,
        nombre_apellido: values.nombre_apellido,
        direccion: values.direccion,
        telefono: values.telefono,
        id_sector: values.id_sector || null
      };

      if (editingMozo) {
        await updateMozo(editingMozo.id, payload);
        setAlert({ variant: 'success', message: 'Mozo modificado exitosamente' });
      } else {
        await createMozo(payload);
        setAlert({ variant: 'success', message: 'Mozo creado exitosamente' });
      }

      setShowModal(false);
      resetForm();
      loadMozos();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteMozo(deletingMozo.id);
      setAlert({ variant: 'success', message: 'Mozo dado de baja exitosamente' });
      setShowDeleteModal(false);
      setDeletingMozo(null);
      loadMozos();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const handleFiltroChange = (campo, valor) => {
    setFiltros(prev => ({ ...prev, [campo]: valor || '' }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handleLimpiarFiltros = () => {
    setFiltros({ activos: '', sector_id: '' });
    setBusqueda('');
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
    loadMozos(page);
  };

  if (loading && mozos.length === 0) {
    return <Cargador />;
  }

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Gestión de Mozos" 
        backPath="/gestion"
        onCreate={handleCreate}
        createLabel="+ Nuevo Mozo"
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)} className="mb-3">
          {alert.message}
        </Alert>
      )}

      <FiltrosMozos
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        busqueda={busqueda}
        onBusquedaChange={setBusqueda}
        onLimpiar={handleLimpiarFiltros}
        sectores={sectores}
        totalMozos={pagination.total}
        mozosFiltrados={mozosFiltrados.length}
      />

      <TablaMozos
        mozos={mozosFiltrados}
        sectores={sectores}
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

      <ModalMozo
        show={showModal}
        onHide={() => setShowModal(false)}
        editingMozo={editingMozo}
        onSubmit={handleSubmit}
        sectores={sectores}
      />

      <ModalBajaMozo
        show={showDeleteModal}
        onHide={() => setShowDeleteModal(false)}
        mozo={deletingMozo}
        onConfirm={handleConfirmDelete}
      />
    </Container>
  );
};

export default Mozos;