import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useSeccionService } from '../../services/seccionService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import Paginacion from '../../components/common/Paginacion';
import FiltroSecciones from './components/FiltroSecciones';
import TablaSecciones from './components/TablaSecciones';
import ModalSeccion from './components/ModalSecciones';
import ModalBajaSeccion from './components/ModalBajaSeccion';

const Secciones = () => {
  const { getSecciones, createSeccion, updateSeccion, deleteSeccion, loading } = useSeccionService();

  const [secciones, setSecciones] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingSeccion, setEditingSeccion] = useState(null);
  const [deletingSeccion, setDeletingSeccion] = useState(null);
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
    activos: ''
  });
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    loadSecciones();
  }, []);

  useEffect(() => {
    loadSecciones();
  }, [pagination.page]);

  const loadSecciones = async (page = pagination.page) => {
    try {
      const filters = {
        page,
        per_page: pagination.per_page,
      };

      const response = await getSecciones(filters);
      let seccionesData = response.data || [];

      if (busqueda) {
        const searchLower = busqueda.toLowerCase();
        seccionesData = seccionesData.filter(s =>
          s.nombre.toLowerCase().includes(searchLower)
        );
      }

      setSecciones(seccionesData);

      if (response.pagination) {
        setPagination(response.pagination);
      }
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const seccionesFiltradas = useMemo(() => {
    let filtered = [...secciones];
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(s => s.nombre.toLowerCase().includes(searchLower));
    }
    return filtered;
  }, [secciones, busqueda]);

  const handleCreate = () => {
    setEditingSeccion(null);
    setShowModal(true);
  };

  const handleEdit = (seccion) => {
    setEditingSeccion(seccion);
    setShowModal(true);
  };

  const handleDelete = (seccion) => {
    setDeletingSeccion(seccion);
    setShowDeleteModal(true);
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      const payload = {
        nombre: values.nombre,
        baja: values.baja || false
      };

      if (editingSeccion) {
        await updateSeccion(editingSeccion.id_seccion, payload);
        setAlert({ variant: 'success', message: 'Sección modificada exitosamente' });
      } else {
        await createSeccion(payload);
        setAlert({ variant: 'success', message: 'Sección creada exitosamente' });
      }

      setShowModal(false);
      resetForm();
      loadSecciones();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteSeccion(deletingSeccion.id_seccion);
      setAlert({ variant: 'success', message: 'Sección dada de baja exitosamente' });
      setShowDeleteModal(false);
      setDeletingSeccion(null);
      loadSecciones();
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
    setFiltros({ activos: '' });
    setBusqueda('');
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
    loadSecciones(page);
  };

  if (loading && secciones.length === 0) {
    return <Cargador />;
  }

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Gestión de Secciones" 
        backPath="/gestion"
        onCreate={handleCreate}
        createLabel="+ Nueva Sección"
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)} className="mb-3">
          {alert.message}
        </Alert>
      )}

      <FiltroSecciones
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        busqueda={busqueda}
        onBusquedaChange={setBusqueda}
        onLimpiar={handleLimpiarFiltros}
        totalSecciones={pagination.total}
        seccionesFiltradas={seccionesFiltradas.length}
      />

      <TablaSecciones
        secciones={seccionesFiltradas}
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

      <ModalSeccion
        show={showModal}
        onHide={() => setShowModal(false)}
        editingSeccion={editingSeccion}
        onSubmit={handleSubmit}
      />

      <ModalBajaSeccion
        show={showDeleteModal}
        onHide={() => setShowDeleteModal(false)}
        seccion={deletingSeccion}
        onConfirm={handleConfirmDelete}
      />
    </Container>
  );
};

export default Secciones;
