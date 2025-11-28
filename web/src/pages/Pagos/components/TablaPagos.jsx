import React, { useEffect, useState } from 'react'
import { Table, Spinner, Alert, Badge } from 'react-bootstrap'
import Paginacion from '../../../components/common/Paginacion'

export default function TablaPagos({ refreshKey, filtros, busqueda, pagination, setPagination }){
  const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099'
  const [pagos, setPagos] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const loadPagos = (page = 1) => {
    setLoading(true)
    setError(null)
    
    const params = new URLSearchParams({
      page: page,
      per_page: pagination.per_page
    })
    
    if (filtros?.id_medio_pago) params.append('id_medio_pago', filtros.id_medio_pago)
    if (filtros?.fecha_desde) params.append('fecha_desde', filtros.fecha_desde)
    if (filtros?.fecha_hasta) params.append('fecha_hasta', filtros.fecha_hasta)
    if (busqueda) params.append('search', busqueda)

    fetch(`${BACKEND}/api/pagos/?${params.toString()}`)
      .then(r=>r.json())
      .then(j=>{ 
        if(j.status==='success') {
          setPagos(j.data || [])
          if (j.pagination) {
            setPagination(j.pagination)
          }
        } else {
          setError(j.message || 'Error al cargar los pagos')
        }
      })
      .catch(err => {
        setError('Error al conectar con el servidor')
        console.error(err)
      })
      .finally(()=>setLoading(false))
  }

  useEffect(()=>{
    loadPagos(pagination.page) 
  },[refreshKey, pagination.page, filtros, busqueda])

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }))
  }

  const formatMonto = (monto) => {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 2
    }).format(monto)
  }

  const formatFecha = (fecha) => {
    if (!fecha) return '-'
    try {
      const dateStr = fecha.includes('T') ? fecha : fecha.replace(' ', 'T')
      const date = new Date(dateStr)
      
      if (isNaN(date.getTime())) return fecha

      return date.toLocaleString('es-AR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return fecha
    }
  }

  if (loading && pagos.length === 0) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      </div>
    )
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>
  }

  return (
    <div>
      {loading && pagos.length > 0 && (
        <div className="text-center my-2 text-muted">
          <Spinner animation="border" size="sm" className="me-2" />
          Actualizando...
        </div>
      )}
      
      {pagos.length === 0 && !loading ? (
        <Alert variant="info" className="text-center">
          No hay pagos registrados. Crea uno nuevo para comenzar.
        </Alert>
      ) : (
        <>
          <div className="table-responsive">
            <Table striped bordered hover className="shadow-sm align-middle">
              <thead className="table-light">
                <tr>
                  <th>ID</th>
                  <th>Factura</th>
                  <th>Medio de Pago</th>
                  <th className="text-end">Monto</th>
                  <th>Fecha</th>
                </tr>
              </thead>
              <tbody>
                {pagos.map(p=> (
                  <tr key={p.id_pago}>
                    <td>
                      <span className="text-muted">#{p.id_pago}</span>
                    </td>
                    <td>
                      {p.factura_codigo ? (
                        <Badge bg="info" className="text-dark">
                          {p.factura_codigo}
                        </Badge>
                      ) : (
                        <span className="text-muted">ID: {p.id_factura}</span>
                      )}
                    </td>
                    <td>
                      {p.medio_pago_nombre ? (
                        <Badge bg="secondary">
                          {p.medio_pago_nombre}
                        </Badge>
                      ) : (
                        <span className="text-muted">ID: {p.id_medio_pago}</span>
                      )}
                    </td>
                    <td className="text-end fw-bold text-success">
                      {formatMonto(parseFloat(p.monto || 0))}
                    </td>
                    <td>
                      <small className="text-muted">
                        {formatFecha(p.fecha)}
                      </small>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>

          <Paginacion 
            currentPage={pagination.page}
            totalPages={pagination.total_pages}
            hasNext={pagination.has_next}
            hasPrev={pagination.has_prev}
            onPageChange={handlePageChange}
          />
        </>
      )}
    </div>
  )
}
