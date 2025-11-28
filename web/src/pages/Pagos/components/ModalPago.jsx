import React, { useState, useEffect } from 'react'
import { Modal, Button } from 'react-bootstrap'

export default function ModalPago({ show = true, onClose, onSuccess }){
  const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099'
  const [idFactura, setIdFactura] = useState('')
  const [idMedioPago, setIdMedioPago] = useState('')
  const [monto, setMonto] = useState('')
  const [fecha, setFecha] = useState('')
  const [medios, setMedios] = useState([])
  const [facturas, setFacturas] = useState([])
  const [error, setError] = useState(null)
  const [loadingMedios, setLoadingMedios] = useState(false)
  const [loadingFacturas, setLoadingFacturas] = useState(false)

  useEffect(()=>{
    if (!show) return
    
    let mounted = true
    setLoadingMedios(true)
    setLoadingFacturas(true)
    
    // Cargar medios de pago
    fetch(`${BACKEND}/api/medio-pagos/`)
      .then(r=>r.json())
      .then(j=>{ if(mounted && j.status==='success') setMedios(j.data) })
      .catch(err => { if(mounted) setError('No se pudieron cargar los medios de pago') })
      .finally(()=> { if(mounted) setLoadingMedios(false) })
    
    // Cargar facturas impagas
    fetch(`${BACKEND}/api/facturas/?solo_impagas=true&per_page=100`)
      .then(r=>r.json())
      .then(j=>{ 
        if(mounted && j.status==='success') {
          setFacturas(j.data || [])
        }
      })
      .catch(err => { 
        if(mounted) setError('No se pudieron cargar las facturas impagas') 
      })
      .finally(()=> { if(mounted) setLoadingFacturas(false) })
    
    return () => { mounted = false }
  }, [show, BACKEND])

  // Autocompletar monto cuando se selecciona una factura
  useEffect(() => {
    if (idFactura) {
      const facturaSeleccionada = facturas.find(f => f.id_factura === parseInt(idFactura))
      if (facturaSeleccionada && facturaSeleccionada.saldo_pendiente) {
        setMonto(facturaSeleccionada.saldo_pendiente.toString())
      }
    } else {
      setMonto('')
    }
  }, [idFactura, facturas])

  // Resetear campos al cerrar el modal
  useEffect(() => {
    if (!show) {
      setIdFactura('')
      setIdMedioPago('')
      setMonto('')
      setFecha('')
      setError(null)
    }
  }, [show])

  const handleSubmit = async (e) =>{
    e.preventDefault()
    setError(null)
    
    // Validaciones
    if (!idFactura) {
      setError('Debe seleccionar una factura')
      return
    }
    if (!idMedioPago) {
      setError('Debe seleccionar un medio de pago')
      return
    }
    if (!monto || parseFloat(monto) <= 0) {
      setError('El monto debe ser mayor a 0')
      return
    }
    if (!fecha) {
      setError('Debe ingresar la fecha del pago')
      return
    }
    
    try{
      const res = await fetch(`${BACKEND}/api/pagos/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          id_factura: parseInt(idFactura), 
          id_medio_pago: parseInt(idMedioPago), 
          monto: parseFloat(monto), 
          fecha 
        })
      })
      const json = await res.json()
      if(json.status === 'success'){
        onSuccess()
      } else {
        setError(json.message || 'Error al crear pago')
      }
    } catch(err){
      setError(err.message || 'Error al crear el pago')
    }
  }

  return (
    <Modal show={show} onHide={onClose}>
      <form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Nuevo Pago</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="mb-2">
            <label className="form-label">Factura <span className="text-danger">*</span></label>
            <select 
              className="form-select" 
              value={idFactura} 
              onChange={e=>setIdFactura(e.target.value)}
              disabled={loadingFacturas}
              required
            >
              <option value="">-- seleccionar factura impaga --</option>
              {facturas.map(f => (
                <option key={f.id_factura} value={f.id_factura}>
                  {f.codigo} - Cliente: {f.cliente?.nombre || 'N/A'} - Saldo: ${f.saldo_pendiente?.toFixed(2) || '0.00'}
                </option>
              ))}
            </select>
            {loadingFacturas && <small className="text-muted">Cargando facturas...</small>}
            {!loadingFacturas && facturas.length === 0 && (
              <small className="text-muted">No hay facturas impagas</small>
            )}
          </div>
          
          {idFactura && (() => {
            const facturaSeleccionada = facturas.find(f => f.id_factura === parseInt(idFactura))
            return facturaSeleccionada && (
              <div className="mb-2 p-2 bg-light rounded">
                <small>
                  <strong>Total factura:</strong> ${facturaSeleccionada.total?.toFixed(2) || '0.00'} | 
                  <strong> Pagado:</strong> ${facturaSeleccionada.total_pagado?.toFixed(2) || '0.00'} | 
                  <strong> Saldo pendiente:</strong> ${facturaSeleccionada.saldo_pendiente?.toFixed(2) || '0.00'}
                </small>
              </div>
            )
          })()}
          
          <div className="mb-2">
            <label className="form-label">Medio de Pago <span className="text-danger">*</span></label>
            <select 
              className="form-select" 
              value={idMedioPago} 
              onChange={e=>setIdMedioPago(e.target.value)}
              disabled={loadingMedios}
              required
            >
              <option value="">-- seleccionar --</option>
              {medios.map(m=> <option key={m.id_medio_pago} value={m.id_medio_pago}>{m.nombre}</option>)}
            </select>
            {loadingMedios && <small className="text-muted">Cargando medios de pago...</small>}
          </div>
          
          <div className="mb-2">
            <label className="form-label">Monto <span className="text-danger">*</span></label>
            <input 
              type="number" 
              step="0.01" 
              min="0.01"
              className="form-control" 
              value={monto} 
              onChange={e=>setMonto(e.target.value)}
              required
            />
            <small className="text-muted">Se autocompleta con el saldo pendiente al seleccionar una factura</small>
          </div>
          
          <div className="mb-2">
            <label className="form-label">Fecha <span className="text-danger">*</span></label>
            <input 
              type="datetime-local" 
              className="form-control" 
              value={fecha ? fecha.replace(' ', 'T').slice(0, 16) : ''}
              onChange={e=>{
                const value = e.target.value
                // Convertir de datetime-local (YYYY-MM-DDTHH:mm) a formato YYYY-MM-DD HH:MM:SS
                if (value) {
                  const formatted = value.replace('T', ' ') + ':00'
                  setFecha(formatted)
                } else {
                  setFecha('')
                }
              }}
              required
            />
          </div>

          {error && <div className="alert alert-danger">{error}</div>}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button variant="primary" type="submit">Crear</Button>
        </Modal.Footer>
      </form>
    </Modal>
  )
}
