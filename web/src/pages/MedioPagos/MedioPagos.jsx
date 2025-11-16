import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useMedioPagoService } from '../../services/medioPagoService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosMedioPagos from './components/FiltrosMedioPagos';
import TablaMedioPagos from './components/TablaMedioPagos';
import ModalMedioPagos from './components/ModalMedioPagos';
import ModalBajaMedioPagos from './components/ModalBajaMedioPagos';
import Paginacion from '../../components/common/Paginacion';

const MedioPagos = () => {
  const { getMedioPagos, createMedioPago, updateMedioPago, deleteMedioPago, loading } = useMedioPagoService();
  const [medioPagos, setMedioPagos] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [editingMedioPago, setEditingMedioPago] = useState(null);
    const [deletingMedioPago, setDeletingMedioPago] = useState(null);
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
    const [busqueda, setBusqueda] = useState('');
    const [filtros, setFiltros] = useState({
        estado: ''
    });

    useEffect(() => {
        loadMedioPagos();
    }, []);

    useEffect(() => {
        // Recargar cuando cambian los filtros o la página
        loadMedioPagos();
    }, [pagination.page, filtros.estado]);
    const loadMedioPagos = async (page = pagination.page) => {
        try {
            const filters = {   
                page,
                per_page: pagination.per_page,
                estado: filtros.estado || undefined,
                search: busqueda || undefined
            };
            const response = await getMedioPagos(filters);
            
            // Aplicar búsqueda local si hay texto de búsqueda
            let medioPagosData = response.data || [];
            if (busqueda) {
                const busquedaLower = busqueda.toLowerCase();
                medioPagosData = medioPagosData.filter(medioPago => 
                    medioPago.nombre.toLowerCase().includes(busquedaLower) ||
                    (medioPago.descripcion && medioPago.descripcion.toLowerCase().includes(busquedaLower))
                );
            }
            setMedioPagos(medioPagosData);


            if (response.pagination) {
        setPagination(response.pagination);
      }
        } catch (error) {
           setAlert({ variant: 'danger', message: error.message });
        }
    };

  const filteredMedioPagos = useMemo(() => {
    let filtered = [...medioPagos];
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(medioPagos => 
        medioPagos.nombre.toLowerCase().includes(searchLower)
      );
    }

    return filtered;
  }, [medioPagos, filtros, busqueda]);

  const handleCreate = () => {
    setEditingMedioPago(null);
    setShowModal(true);
  };

  const handleEdit = (medioPago) => {
    setEditingMedioPago(medioPago);
    setShowModal(true);
  };

  const handleDelete = (medioPago) => {
    setDeletingMedioPago(medioPago);
    setShowDeleteModal(true);
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      if (editingMedioPago) {
        await updateMedioPago(editingMedioPago.id_medio_pago, values);
        setAlert({ variant: 'success', message: 'Medio de pago actualizado correctamente.' });
      } else {
        await createMedioPago(values);
        setAlert({ variant: 'success', message: 'Medio de pago creado correctamente.' });
      }
        setShowModal(false);
        resetForm();
        loadMedioPagos();
        setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
        setSubmitting(false);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteMedioPago(deletingMedioPago.id_medio_pago);
      setAlert({ variant: 'success', message: 'Medio de pago eliminado correctamente.' });
        setShowDeleteModal(false);
        setDeletingMedioPago(null);
        loadMedioPagos();
        setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    };
    };
    const handleFiltroChange = (campo, valor) => {
        setFiltros((prevFiltros) => ({ ...prevFiltros, [campo]: valor || '' }));
        // Resetear a página 1 cuando cambian los filtros
    setPagination(prev => ({ ...prev, page: 1 }));
    };

    const handleLimpiarFiltros = () => {
        setFiltros({
            estado: ''
        });
        setBusqueda('');
        setPagination(prev => ({ ...prev, page: 1 }));
    };

    const handlePageChange = (page) => {
        setPagination(prev => ({ ...prev, page }));
        loadMedioPagos(page);
    };

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Medios de Pago" 
        backPath="/gestion"
        onCreate={handleCreate}
        createLabel="+ Nuevo Medio de Pago"
      />  

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)} className="mb-3">
          {alert.message}
        </Alert>
      )}

            <FiltrosMedioPagos
                filtros={filtros}
                onFiltroChange={handleFiltroChange}
                busqueda={busqueda }
                onBusquedaChange={setBusqueda}
                onLimpiar={handleLimpiarFiltros}
                
                />
  

            <TablaMedioPagos
                medioPagos={filteredMedioPagos}
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
            <ModalMedioPagos
                show={showModal}
                onHide={() => setShowModal(false)}
                editingMedioPago={editingMedioPago }
                onSubmit={handleSubmit}
            />
            <ModalBajaMedioPagos
                show={showDeleteModal}
                onHide={() => setShowDeleteModal(false)}
                medioPago={deletingMedioPago}
                onConfirm={handleConfirmDelete}
            />
        </Container>
  );
};

export default MedioPagos;