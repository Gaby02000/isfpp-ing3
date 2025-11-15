import React, { useState, useEffect } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
// 1. Importar el servicio de cliente
import { useClienteService } from '../../services/clienteService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
// 2. Importar los componentes de cliente
import FiltrosClientes from './components/FiltrosClientes';
import TablaClientes from './components/TablaClientes';
import ModalCliente from './components/ModalCliente';
import ModalBajaCliente from './components/ModalBajaCliente';
import Paginacion from '../../components/common/Paginacion';

const Clientes = () => {
  // 3. Usar el hook de cliente
  const { getClientes, createCliente, updateCliente, deleteCliente, loading } = useClienteService();
  
  // 4. Renombrar estados
  const [clientes, setClientes] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingCliente, setEditingCliente] = useState(null);
  const [deletingCliente, setDeletingCliente] = useState(null);
  const [alert, setAlert] = useState(null);
  
  // Paginación (sin cambios)
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 1,
    has_next: false,
    has_prev: false
  });
  
  // 5. Actualizar los filtros
  const [filtros, setFiltros] = useState({
    documento: '',
    nombre: '',
    apellido: ''
  });
  // 6. 'busqueda' local eliminada (ahora todo lo maneja el backend)

  useEffect(() => {
    // 7. Cargar clientes al montar
    loadClientes();
  }, []);

  useEffect(() => {
    // 8. Recargar cuando cambian los filtros o la página
    loadClientes();
  }, [pagination.page, filtros.documento, filtros.nombre, filtros.apellido]);

  const loadClientes = async (page = pagination.page) => {
    try {
      // 9. Construir filtros para clientes
      const filters = {
        page,
        per_page: pagination.per_page,
        documento: filtros.documento || undefined,
        nombre: filtros.nombre || undefined,
        apellido: filtros.apellido || undefined
      };
      
      const response = await getClientes(filters);
      
      setClientes(response.data || []);
      
      if (response.pagination) {
        setPagination(response.pagination);
      }
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  // 10. loadSectores y loadTiposMesas eliminados

  // 11. 'useMemo' para búsqueda local eliminado

  // 12. Renombrar manejadores de eventos
  const handleCreate = () => {
    setEditingCliente(null);
    setShowModal(true);
  };

  const handleEdit = (cliente) => {
    setEditingCliente(cliente);
    setShowModal(true);
  };

  const handleDelete = (cliente) => {
    setDeletingCliente(cliente);
    setShowDeleteModal(true);
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      // 13. Lógica de guardado para cliente
      if (editingCliente) {
        await updateCliente(editingCliente.id_cliente, values);
        setAlert({ variant: 'success', message: 'Cliente modificado exitosamente' });
      } else {
        await createCliente(values);
        setAlert({ variant: 'success', message: 'Cliente creado exitosamente' });
      }
      setShowModal(false);
      resetForm();
      loadClientes(); // Recargar
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      // 14. Lógica de borrado para cliente
      await deleteCliente(deletingCliente.id_cliente);
      setAlert({ variant: 'success', message: 'Cliente dado de baja exitosamente' });
      setShowDeleteModal(false);
      setDeletingCliente(null);
      loadClientes(); // Recargar
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
    // 15. Limpiar filtros de cliente
    setFiltros({
      documento: '',
      nombre: '',
      apellido: ''
    });
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
    loadClientes(page);
  };

  // 16. Condición de carga
  if (loading && clientes.length === 0) {
    return <Cargador />;
  }

  return (
    <Container fluid className="py-4">
      {/* 17. Títulos actualizados */}
      <PageHeader 
        title="Gestión de Clientes" 
        backPath="/gestion" 
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)}>
          {alert.message}
        </Alert>
      )}

      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Listado de Clientes</h2>
        <Button variant="primary" onClick={handleCreate}>
          + Nuevo Cliente
        </Button>
      </div>

      {/* 18. Componente de Filtros de Cliente */}
      <FiltrosClientes
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        onLimpiar={handleLimpiarFiltros}
        totalClientes={pagination.total} // Total de resultados encontrados
        clientesFiltrados={clientes.length} // Mostrados en esta página
      />

      {/* 19. Componente de Tabla de Cliente */}
      <TablaClientes
        clientes={clientes} // Pasa la lista de clientes (ya filtrada por backend)
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

      {/* 20. Componente de Modal de Cliente */}
      <ModalCliente
        show={showModal}
        onHide={() => setShowModal(false)}
        editingCliente={editingCliente}
        onSubmit={handleSubmit}
        // Sin props extra (sectores/tipos)
      />

      {/* 21. Componente de Modal de Baja de Cliente */}
      <ModalBajaCliente
        show={showDeleteModal}
        onHide={() => setShowDeleteModal(false)}
        cliente={deletingCliente}
        onConfirm={handleConfirmDelete}
      />
    </Container>
  );
};

export default Clientes;