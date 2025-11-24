import React, { useState, useEffect } from 'react'
import { Modal, Button } from 'react-bootstrap'

export default function ModalPago({ show = true, onClose, onSuccess }){
  const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099'
  const [idFactura, setIdFactura] = useState('')
  const [idMedioPago, setIdMedioPago] = useState('')
  const [monto, setMonto] = useState('')
  const [fecha, setFecha] = useState('')
  const [medios, setMedios] = useState([])
  const [error, setError] = useState(null)
  const [loadingMedios, setLoadingMedios] = useState(false)

  useEffect(()=>{
    let mounted = true
    setLoadingMedios(true)
    fetch(`${BACKEND}/api/medio-pagos/`)
      .then(r=>r.json())
      .then(j=>{ if(mounted && j.status==='success') setMedios(j.data) })
      .catch(err => { if(mounted) setError('No se pudieron cargar los medios de pago') })
      .finally(()=> { if(mounted) setLoadingMedios(false) })
    return () => { mounted = false }
  },[])

  const handleSubmit = async (e) =>{
    e.preventDefault()
    setError(null)
    try{
  const res = await fetch(`${BACKEND}/api/pagos/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_factura: idFactura, id_medio_pago: idMedioPago, monto, fecha })
      })
      const json = await res.json()
      if(json.status === 'success'){
        onSuccess()
      } else {
        setError(json.message || 'Error al crear pago')
      }
    } catch(err){
      setError(err.message)
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
            <label className="form-label">Id Factura</label>
            <input className="form-control" value={idFactura} onChange={e=>setIdFactura(e.target.value)} />
          </div>
          <div className="mb-2">
            <label className="form-label">Medio de Pago</label>
            <select className="form-select" value={idMedioPago} onChange={e=>setIdMedioPago(e.target.value)}>
              <option value="">-- seleccionar --</option>
              {medios.map(m=> <option key={m.id_medio_pago} value={m.id_medio_pago}>{m.nombre}</option>)}
            </select>
          </div>
          <div className="mb-2">
            <label className="form-label">Monto</label>
            <input className="form-control" value={monto} onChange={e=>setMonto(e.target.value)} />
          </div>
          <div className="mb-2">
            <label className="form-label">Fecha</label>
            <input className="form-control" value={fecha} onChange={e=>setFecha(e.target.value)} placeholder="YYYY-MM-DD HH:MM:SS" />
          </div>

          {error && <div className="text-danger">{error}</div>}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button variant="primary" type="submit">Crear</Button>
        </Modal.Footer>
      </form>
    </Modal>
  )
}
