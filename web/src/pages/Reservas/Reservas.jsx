import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useReservaService } from '../../services/reservaService';
import { useClienteService } from '../../services/clienteService';
import { useMesaService } from '../../services/mesaService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosReserva from './components/FiltrosReserva';
import TablaReservas from './components/TablaReservas';
import ModalReservas from './components/ModalReservas';
import ModalBajaReserva from './components/ModalBajaReserva';
import ModalDetalleReserva from './components/ModalDetalleReserva';
import Paginacion from '../../components/common/Paginacion';

const Reservas = () => {
  const { getReservas, getReserva, createReserva, updateReserva, cancelarReserva, loading } = useReservaService();
  const { getClientes } = useClienteService();
  const { getMesas } = useMesaService();

  const [reservas, setReservas] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [mesas, setMesas] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [editingReserva, setEditingReserva] = useState(null);
  const [cancelingReserva, setCancelingReserva] = useState(null);
  const [detalleReserva, setDetalleReserva] = useState(null);
  const [showDetalleModal, setShowDetalleModal] = useState(false);
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
    cancelado: '',
    cliente_id: '',
    fecha_desde: '',
    fecha_hasta: '',
    cant_min: '',
    cant_max: ''
  });

  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    loadReservas();
    loadClientes();
    loadMesas();
  }, []);

  useEffect(() => {
    loadReservas();
  }, [pagination.page, filtros.cancelado, filtros.cliente_id, filtros.fecha_desde, filtros.fecha_hasta, filtros.cant_min, filtros.cant_max]);

  const loadReservas = async (page = pagination.page) => {
    try {
      const filters = {
        page,
        per_page: pagination.per_page,
        cancelado: filtros.cancelado || undefined,
        cliente_id: filtros.cliente_id || undefined,
        fecha_desde: filtros.fecha_desde || undefined,
        fecha_hasta: filtros.fecha_hasta || undefined,
        // opcionales: cant_min/cant_max pueden manejarse en frontend o pasarse al backend si se implementa
        //cant_min: filtros.cant_min || undefined,
        //cant_max: filtros.cant_max || undefined,
        order_by: filtros.order_by || undefined
      };

      const response = await getReservas(filters);
      let reservasData = response.data || [];

      if (busqueda) {
        const searchLower = busqueda.toLowerCase();
        reservasData = reservasData.filter(r =>
          String(r.numero).toLowerCase().includes(searchLower)
        );
      }

      setReservas(reservasData);

      if (response.pagination) {
        setPagination(response.pagination);
      }
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const loadClientes = async () => {
    try {
      const response = await getClientes();
      setClientes(response.data || []);
    } catch {
      setClientes([]);
    }
  };

  const loadMesas = async () => {
    try {
      const response = await getMesas();
      setMesas(response.data || []);
    } catch {
      setMesas([]);
    }
  };

  const reservasFiltradas = useMemo(() => {
    let filtered = [...reservas];
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(r =>
        String(r.numero).toLowerCase().includes(searchLower)
      );
    }
    return filtered;
  }, [reservas, busqueda]);

  const handleCreate = () => {
    setEditingReserva(null);
    setShowModal(true);
  };

  const handleEdit = (reserva) => {
    setEditingReserva(reserva);
    setShowModal(true);
  };

  const handleCancel = (reserva) => {
    setCancelingReserva(reserva);
    setShowCancelModal(true);
  };

  const handleView = async (reserva) => {
    try {
      const resp = await getReserva(reserva.id_reserva);
      // resp is axios response.data (backend wrapper { status, data })
      const detalle = resp.data || resp;
      setDetalleReserva(detalle);
      setShowDetalleModal(true);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      const payload = {
        numero: values.numero,
        fecha_hora: values.fecha_hora,
        cant_personas: values.cant_personas,
        id_cliente: values.id_cliente,
        id_mesa: values.id_mesa
      };

      if (editingReserva) {
        await updateReserva(editingReserva.id_reserva, payload);
        setAlert({ variant: 'success', message: 'Reserva modificada exitosamente' });
      } else {
        await createReserva(payload);
        setAlert({ variant: 'success', message: 'Reserva creada exitosamente' });
      }

      setShowModal(false);
      resetForm();
      loadReservas();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  // onConfirm desde el ModalBajaReserva pasará un objeto { motivo, senia_devuelta }
  const handleConfirmCancel = async (body) => {
    try {
      await cancelarReserva(cancelingReserva.id_reserva, body);
      setAlert({ variant: 'success', message: 'Reserva cancelada exitosamente' });
      setShowCancelModal(false);
      setCancelingReserva(null);
      loadReservas();
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
    setFiltros({
      cancelado: '',
      cliente_id: '',
      fecha_desde: '',
      fecha_hasta: '',
      cant_min: '',
      cant_max: ''
    });
    setBusqueda('');
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
    loadReservas(page);
  };

  if (loading && reservas.length === 0) {
    return <Cargador />;
  }

  return (
    <Container fluid className="py-4">
      <PageHeader
        title="Gestión de Reservas"
        backPath="/gestion"
        onCreate={handleCreate}
        createLabel="+ Nueva Reserva"
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)} className="mb-3">
          {alert.message}
        </Alert>
      )}

      <FiltrosReserva
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        busqueda={busqueda}
        onBusquedaChange={setBusqueda}
        onLimpiar={handleLimpiarFiltros}
        clientes={clientes}
        totalReservas={pagination.total}
        reservasFiltradas={reservasFiltradas.length}
      />

      <TablaReservas
        reservas={reservasFiltradas}
        clientes={clientes}
        mesas={mesas}
        onEdit={handleEdit}
        onCancel={handleCancel}
        onView={handleView}
      />

      <Paginacion
        currentPage={pagination.page}
        totalPages={pagination.total_pages}
        hasNext={pagination.has_next}
        hasPrev={pagination.has_prev}
        onPageChange={handlePageChange}
      />

      <ModalReservas
        show={showModal}
        onHide={() => setShowModal(false)}
        editingReserva={editingReserva}
        onSubmit={handleSubmit}
        clientes={clientes}
        mesas={mesas}
      />

      <ModalDetalleReserva
        show={showDetalleModal}
        onHide={() => setShowDetalleModal(false)}
        reserva={detalleReserva}
      />

      <ModalBajaReserva
        show={showCancelModal}
        onHide={() => setShowCancelModal(false)}
        reserva={cancelingReserva}
        onConfirm={handleConfirmCancel}
      />
    </Container>
  );
};

export default Reservas;