import React, { useState } from 'react'
import TablaPagos from './components/TablaPagos'
import ModalPago from './components/ModalPago'

export default function Pagos(){
  const [openModal, setOpenModal] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)

  return (
    <div>
      <h2>Pagos</h2>
      <div style={{marginBottom: 16}}>
        <button className="btn btn-primary" onClick={() => setOpenModal(true)}>Nuevo pago</button>
      </div>

      <TablaPagos refreshKey={refreshKey} />

      {openModal && (
        <ModalPago
          show={openModal}
          onClose={() => setOpenModal(false)}
          onSuccess={() => { setOpenModal(false); setRefreshKey(k => k+1) }}
        />
      )}
    </div>
  )
}
