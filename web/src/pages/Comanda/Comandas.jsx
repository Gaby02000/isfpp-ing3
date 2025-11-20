import React, { useState, useEffect, useMemo } from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useComandaService } from '../../services/comandaService';
import { useMesaService } from '../../services/mesaService';
import { useMozoService } from '../../services/mozoService';
import Cargador from '../../components/common/Cargador';
import PageHeader from '../../components/common/PageHeader';
import FiltrosComandas from './components/FiltrosComandas';
import TablaComandas from './components/TablaComandas';
import ModalComanda from './components/ModalComanda';
import ModalBajaComanda from './components/ModalBajaComanda';
import Paginacion from '../../components/common/Paginacion';

const Comandas = () => {
    const { getComandas, createComanda, updateComanda, deleteComanda, loading } = useComandaService();
    const { getTodasMesas } = useMesaService();
    const { getTodosMozos } = useMozoService();
    const [comandas, setComandas] = useState([]);
    const [mesas, setMesas] = useState([]);
    const [mozos, setMozos] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [editingComanda, setEditingComanda] = useState(null);
    const [deletingComanda, setDeletingComanda] = useState(null);
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
        id_mesa: ''
    });
    const [busqueda, setBusqueda] = useState('');
    useEffect(() => {
        loadComandas();
        loadMesas();
        loadMozos();
    }, []);

    useEffect(() => {
        // Recargar cuando cambian los filtros o la página
        loadComandas();
    }, [pagination.page, filtros.id_mozo, filtros.id_mesa, filtros.fecha]);

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
        

        // Aplicar búsqueda local si hay texto de búsqueda
        let comandasData = response.data || [];
        if (busqueda) {
            const busquedaLower = busqueda.toLowerCase();
            comandasData = comandasData.filter(comanda =>
                comanda.mesa.numero.toString().includes(busquedaLower) ||
                comanda.mozo.nombre.toLowerCase().includes(busquedaLower)
            );
        }

        setComandas(comandasData);
// Actualizar paginación
        if (response.pagination) {  
            setPagination(response.pagination);
        }
    } catch (error) {
        setAlert({ variant: 'danger', message: error.message });
    }

    };

    const loadMesas = async () => {
        try {
            const response = await getTodasMesas();
            setMesas(response.data || []);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

    const loadMozos = async () => {
        try {
            const response = await getTodosMozos();
            setMozos(response.data || []);
        } catch (error) {
            setAlert({ variant: 'danger', message: error.message });
        }
    };

//Filtrar comandas solo por busqueda (filtros ya vienen del backend)
    const comandasFiltradas = useMemo(() => {
        let filtered = [...comandas];
        if (busqueda) {
            const busquedaLower = busqueda.toLowerCase();
            filtered = filtered.filter(comanda =>
                comanda.mesa.numero.toString().includes(busquedaLower) ||
                comanda.mozo.nombre.toLowerCase().includes(busquedaLower)
            );
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
    }

    const handleSubmit = async (values,{ setSubmitting, resetForm}) => {
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
            setAlert({ variant: 'success', message: 'Comanda dada de baja correctamente.' });   
            setShowDeleteModal(false);
            setDeletingComanda(null);
            loadComandas();
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

  if (loading && comandas.length === 0) {
    return <Cargador />;
  }
    return (
        <Container fluid className="p-4">
            <PageHeader title="Comandas" 
            backPath="/gestion"
        onCreate={handleCreate}
        createLabel="+ Nueva Comanda"
            />  
            {alert && <Alert variant={alert.variant}>{alert.message}</Alert>}
            <FiltrosComandas 
                filtros={filtros}
                onFiltroChange={handleFiltroChange}
                onLimpiarFiltros={handleLimpiarFiltros}
                busqueda={busqueda}
                onBusquedaChange={setBusqueda}
                mesas={mesas}
                mozos={mozos}
                comandasFiltradas={comandasFiltradas.length}
            />
            <TablaComandas 
                comandas={comandasFiltradas}
                onEdit={handleEdit}
                onDelete={handleDelete}
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
            />
            <ModalBajaComanda
        show={showDeleteModal}
        onHide={() => setShowDeleteModal(false)}
        comanda={deletingComanda}
        onConfirm={handleConfirmDelete}
        />
        </Container>
    );
}
export default Comandas;
