import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useComandaService } from '../../services/comandaService';
import { useMesaService } from '../../services/mesaService';
import { useMozoService } from '../../services/mozoService';
import { useProductoService } from '../../services/productoService';
import { useFacturaService } from '../../services/facturaService';
import { useClienteService } from '../../services/clienteService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosComandas from './components/FiltrosComandas';
import TablaComandas from './components/TablaComandas';
import ModalComanda from './components/ModalComanda';
import ModalBajaComanda from './components/ModalBajaComanda';
import ModalGenerarFactura from './components/ModalGenerarFactura';
import ModalVerFactura from './components/ModalVerFactura';
import Paginacion from '../../components/common/Paginacion';

const Comandas = () => {
    const { getComandas, createComanda, updateComanda, deleteComanda, loading } = useComandaService();
    const { getMesasDisponibles } = useMesaService();
    const { getMozos } = useMozoService();
    const { getProductos } = useProductoService();
    const { generarFacturaDesdeComanda } = useFacturaService();
    const { getClientes } = useClienteService();

    const [comandas, setComandas] = useState([]);
    const [mesas, setMesas] = useState([]);
    const [mozos, setMozos] = useState([]);
    const [productos, setProductos] = useState([]);
    const [clientes, setClientes] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showFacturaModal, setShowFacturaModal] = useState(false);
    const [showVerFacturaModal, setShowVerFacturaModal] = useState(false);
    const [editingComanda, setEditingComanda] = useState(null);
    const [deletingComanda, setDeletingComanda] = useState(null);
    const [facturandoComanda, setFacturandoComanda] = useState(null);
    const [facturaGenerada, setFacturaGenerada] = useState(null);
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
        fecha: '',
        id_mozo: '',
        id_mesa: '',
        estado: ''
    });
    const [busqueda, setBusqueda] = useState('');

    useEffect(() => {
        loadComandas();
        loadMesas();
        loadMozos();
        loadProductos();
        loadClientes();
    }, []);

    useEffect(() => {
        loadComandas();
    }, [pagination.page, filtros.id_mozo, filtros.id_mesa, filtros.fecha, filtros.estado]);

    const loadComandas = async (page = pagination.page) => {
        try {
            const filters = {
                page,
                per_page: pagination.per_page,
                id_mozo: filtros.id_mozo || undefined,
                id_mesa: filtros.id_mesa || undefined,
                fecha: filtros.fecha || undefined,
                estado: filtros.estado || undefined
            };
            const response = await getComandas(filters);

            let comandasData = response.data || [];
            setComandas(comandasData);

            if (response.pagination) {  
                setPagination(response.pagination);
            }
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

    const loadMesas = async () => {
        try {
            const response = await getMesasDisponibles();
            setMesas(response.data || []);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

    const loadMozos = async () => {
        try {
            const response = await getMozos();
            setMozos(response.data || []);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

    const loadProductos = async () => {
        try {
            const response = await getProductos();
            setProductos(response.data || []);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

    const loadClientes = async () => {
        try {
            const response = await getClientes({ activos: 'true' });
            setClientes(response.data || []);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

    const comandasFiltradas = useMemo(() => {
        let filtered = [...comandas];
        if (busqueda) {
            const busquedaLower = busqueda.toLowerCase();
            filtered = filtered.filter(comanda => {
                const matchComanda = comanda.id_comanda?.toString().includes(busquedaLower);
                const matchMesa = comanda.mesa?.numero?.toString().includes(busquedaLower);
                const matchMozo = comanda.mozo?.nombre_apellido?.toLowerCase().includes(busquedaLower);
                return matchComanda || matchMesa || matchMozo;
            });
        }
        return filtered;
    }, [comandas, busqueda]);

    const handleCreate = () => {
        setEditingComanda(null);
        setShowModal(true);
    };

    const handleEdit = (comanda) => {
        setEditingComanda(comanda);
        setShowModal(true);
    };

    const handleDelete = (comanda) => {
        setDeletingComanda(comanda);
        setShowDeleteModal(true);
    };

    const handleGenerarFactura = (comanda) => {
        setFacturandoComanda(comanda);
        setShowFacturaModal(true);
    };

    const handleSubmit = async (values, { setSubmitting, resetForm }) => {
        try {
            if (editingComanda) {
                await updateComanda(editingComanda.id_comanda, values);
                setAlert({ variant: 'success', message: 'Comanda actualizada correctamente.' });
            } else {
                await createComanda(values);
                setAlert({ variant: 'success', message: 'Comanda creada correctamente.' });
            }
            setShowModal(false);
            resetForm();
            loadComandas();
            setTimeout(() => setAlert(null), 3000);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        } finally {
            setSubmitting(false);
        }
    };

    const handleConfirmDelete = async () => {
        try {
            await deleteComanda(deletingComanda.id_comanda);
            setAlert({ variant: 'success', message: 'Comanda cancelada correctamente.' });   
            setShowDeleteModal(false);
            setDeletingComanda(null);
            loadComandas();
            setTimeout(() => setAlert(null), 3000);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

    const handleConfirmGenerarFactura = async (id_cliente) => {
        try {
            const response = await generarFacturaDesdeComanda(
                facturandoComanda.id_comanda,
                id_cliente
            );
            
            setShowFacturaModal(false);
            setFacturaGenerada(response.data);
            setShowVerFacturaModal(true);
            loadComandas();
            setFacturandoComanda(null);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
            setTimeout(() => setAlert(null), 5000);
        }
    };

    const handleFiltroChange = (campo, valor) => {
        setFiltros(prev => ({ ...prev, [campo]: valor || '' }));
        setPagination(prev => ({ ...prev, page: 1 }));
    };

    const handleLimpiarFiltros = () => {
        setFiltros({
            fecha: '',
            id_mozo: '',
            id_mesa: '',
            estado: ''
        });
        setBusqueda('');
        setPagination(prev => ({ ...prev, page: 1 }));
    };

    const handlePageChange = (page) => {
        setPagination(prev => ({ ...prev, page }));
        loadComandas(page);
    };

    if (loading && comandas.length === 0) {
        return <Cargador />;
    }

    return (
        <Container fluid className="p-4">
            <PageHeader 
                title="Comandas" 
                backPath="/gestion"
                onCreate={handleCreate}
                createLabel="+ Nueva Comanda"
            />  
            {alert && <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)}>{alert.message}</Alert>}
            
            <FiltrosComandas 
                filtros={filtros}
                onFiltroChange={handleFiltroChange}
                onLimpiarFiltros={handleLimpiarFiltros}
                busqueda={busqueda}
                onBusquedaChange={setBusqueda}
                mesas={mesas}
                mozos={mozos}
                comandasFiltradas={comandasFiltradas.length}
                totalComandas={pagination.total}
            />
            
            <TablaComandas 
                comandas={comandasFiltradas}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onGenerarFactura={handleGenerarFactura}
            />

            <Paginacion 
                pagination={pagination}
                onPageChange={handlePageChange}
            />
            
            <ModalComanda 
                show={showModal}
                onHide={() => setShowModal(false)}
                onSubmit={handleSubmit}
                comanda={editingComanda}
                mesas={mesas}
                mozos={mozos}
                productos={productos}
            />
            
            <ModalBajaComanda
                show={showDeleteModal}
                onHide={() => setShowDeleteModal(false)}
                comanda={deletingComanda}
                onConfirm={handleConfirmDelete}
            />

            <ModalGenerarFactura
                show={showFacturaModal}
                onHide={() => setShowFacturaModal(false)}
                comanda={facturandoComanda}
                onConfirm={handleConfirmGenerarFactura}
                loading={loading}
                clientes={clientes}
            />

            <ModalVerFactura
                show={showVerFacturaModal}
                onHide={() => {
                    setShowVerFacturaModal(false);
                    setFacturaGenerada(null);
                }}
                factura={facturaGenerada}
            />
        </Container>
    );
};

export default Comandas;