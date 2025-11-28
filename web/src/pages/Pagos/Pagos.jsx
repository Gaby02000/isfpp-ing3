import React, { useState, useEffect } from 'react'
import { Container, Alert, Button } from 'react-bootstrap'
import TablaPagos from './components/TablaPagos'
import ModalPago from './components/ModalPago'
import FiltrosPagos from './components/FiltrosPagos'
import PageHeader from '../../components/common/PageHeader'

export default function Pagos(){
  const [openModal, setOpenModal] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)
  const [alert, setAlert] = useState(null)
  
  // Estado para filtros y paginación (manejado aquí para pasarlo a la tabla)
  const [filtros, setFiltros] = useState({
    fecha_desde: '',
    fecha_hasta: '',
    id_medio_pago: ''
  })
  const [busqueda, setBusqueda] = useState('')
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 1,
    has_next: false,
    has_prev: false
  })

  const handleSuccess = () => {
    setOpenModal(false)
    setRefreshKey(k => k + 1)
    setAlert({ variant: 'success', message: 'Pago registrado exitosamente' })
    setTimeout(() => setAlert(null), 3000)
  }

  const handleFiltroChange = (campo, valor) => {
    setFiltros(prev => ({ ...prev, [campo]: valor }))
    setPagination(prev => ({ ...prev, page: 1 })) // Resetear página al filtrar
  }

  const handleLimpiarFiltros = () => {
    setFiltros({
      fecha_desde: '',
      fecha_hasta: '',
      id_medio_pago: ''
    })
    setBusqueda('')
    setPagination(prev => ({ ...prev, page: 1 }))
  }

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Gestión de Pagos" 
        backPath="/gestion"
        onCreate={() => setOpenModal(true)}
        createLabel="+ Nuevo Pago"
      />

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)} className="mb-3">
          {alert.message}
        </Alert>
      )}

      <FiltrosPagos
        filtros={filtros}
        onFiltroChange={handleFiltroChange}
        busqueda={busqueda}
        onBusquedaChange={(val) => { setBusqueda(val); setPagination(prev => ({...prev, page: 1})) }}
        onLimpiarFiltros={handleLimpiarFiltros}
        totalPagos={pagination.total}
        pagosFiltrados={pagination.total} // En este caso es lo mismo porque el backend filtra
      />

      <TablaPagos 
        refreshKey={refreshKey} 
        filtros={filtros}
        busqueda={busqueda}
        pagination={pagination}
        setPagination={setPagination}
      />

      {openModal && (
        <ModalPago
          show={openModal}
          onClose={() => setOpenModal(false)}
          onSuccess={handleSuccess}
        />
      )}
    </Container>
  )
}
