import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useProductoService } from '../../services/productoService';
import { useSeccionService } from '../../services/seccionService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosProductos from './components/FiltrosProductos';
import TablaProductos from './components/TablaProductos';
import ModalProducto from './components/ModalProductos';
import ModalBajaProducto from './components/ModalBajaProducto';
import Paginacion from '../../components/common/Paginacion';

const Productos = () => {
  const { getProductos, createProducto, updateProducto, deleteProducto, loading } = useProductoService();
  const { getTodasSecciones } = useSeccionService();

  const [productos, setProductos] = useState([]);
  const [secciones, setSecciones] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingProducto, setEditingProducto] = useState(null);
  const [deletingProducto, setDeletingProducto] = useState(null);
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
    id_seccion: '',
    precio_min: '',
    precio_max: ''
  });

  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    loadProductos();
    loadSecciones();
  }, []);

  useEffect(() => {
    loadProductos();
  }, [pagination.page, filtros.activos, filtros.id_seccion, filtros.precio_min, filtros.precio_max]);

  const loadProductos = async (page = pagination.page) => {
    try {
      const filters = {
        page,
        per_page: pagination.per_page,
        activos: filtros.activos || undefined,
        id_seccion: filtros.id_seccion || undefined,
        precio_min: filtros.precio_min || undefined,
        precio_max: filtros.precio_max || undefined
      };

      const response = await getProductos(filters);
      let productosData = response.data || [];

      if (busqueda) {
        const searchLower = busqueda.toLowerCase();
        productosData = productosData.filter(p =>
          p.nombre.toLowerCase().includes(searchLower) ||
          p.codigo.toLowerCase().includes(searchLower)
        );
      }

      setProductos(productosData);

      if (response.pagination) {
        setPagination(response.pagination);
      }
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    }
  };

  const loadSecciones = async () => {
    try {
      const response = await getTodasSecciones();
      setSecciones(response.data || []);
    } catch {
      setSecciones([]);
    }
  };

  const productosFiltrados = useMemo(() => {
    let filtered = [...productos];
    if (busqueda) {
      const searchLower = busqueda.toLowerCase();
      filtered = filtered.filter(p =>
        p.nombre.toLowerCase().includes(searchLower) ||
        p.codigo.toLowerCase().includes(searchLower)
      );
    }
    return filtered;
  }, [productos, busqueda]);

  const handleCreate = () => {
    setEditingProducto(null);
    setShowModal(true);
  };

  const handleEdit = (producto) => {
    setEditingProducto(producto);
    setShowModal(true);
  };

  const handleDelete = (producto) => {
    setDeletingProducto(producto);
    setShowDeleteModal(true);
  };

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      // payload general
      const payload = {
        codigo: values.codigo,
        nombre: values.nombre,
        descripcion: values.descripcion,
        precio: values.precio,
        id_seccion: values.id_seccion || null,
        tipo: values.tipo
      };

      // si es bebida agregar cm3
      if (values.tipo === 'bebida') {
        payload.cm3 = Number(values.cm3);
      }

      if (editingProducto) {
        await updateProducto(editingProducto.id_producto, payload);
        setAlert({ variant: 'success', message: 'Producto modificado exitosamente' });
      } else {
        await createProducto(payload);
        setAlert({ variant: 'success', message: 'Producto creado exitosamente' });
      }

      setShowModal(false);
      resetForm();
      loadProductos();
      setTimeout(() => setAlert(null), 3000);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteProducto(deletingProducto.id_producto);
      setAlert({ variant: 'success', message: 'Producto dado de baja exitosamente' });
      setShowDeleteModal(false);
      setDeletingProducto(null);
      loadProductos();
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
      activos: '',
      id_seccion: '',
      precio_min: '',
      precio_max: ''
    });
    setBusqueda('');
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
    loadProductos(page);
  };

  if (loading && productos.length === 0) {
    return <Cargador />;
  }

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Gestión de Productos" 
        backPath="/gestion"
        onCreate={handleCreate}
        createLabel="+ Nuevo Producto"
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)} className="mb-3">
          {alert.message}
        </Alert>
      )}

      <FiltrosProductos
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        busqueda={busqueda}
        onBusquedaChange={setBusqueda}
        onLimpiar={handleLimpiarFiltros}
        secciones={secciones}
        totalProductos={pagination.total}
        productosFiltrados={productosFiltrados.length}
      />

      <TablaProductos
        productos={productosFiltrados}
        secciones={secciones}
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

      <ModalProducto
        show={showModal}
        onHide={() => setShowModal(false)}
        editingProducto={editingProducto}
        onSubmit={handleSubmit}
        secciones={secciones}
      />

      <ModalBajaProducto
        show={showDeleteModal}
        onHide={() => setShowDeleteModal(false)}
        producto={deletingProducto}
        onConfirm={handleConfirmDelete}
      />
    </Container>
  );
};

export default Productos;
