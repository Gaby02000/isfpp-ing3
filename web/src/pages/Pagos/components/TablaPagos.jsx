import React, { useEffect, useState } from 'react'

export default function TablaPagos({ refreshKey }){
  const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099'
  const [pagos, setPagos] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(()=>{
    setLoading(true)
    fetch(`${BACKEND}/api/pagos/`)
      .then(r=>r.json())
      .then(j=>{ if(j.status==='success') setPagos(j.data) })
      .finally(()=>setLoading(false))
  },[refreshKey])

  return (
    <div>
      {loading && <div>Cargando...</div>}
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Factura</th>
            <th>Medio</th>
            <th>Monto</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {pagos.map(p=> (
            <tr key={p.id_pago}>
              <td>{p.id_pago}</td>
              <td>{p.id_factura}</td>
              <td>{p.id_medio_pago}</td>
              <td>{p.monto}</td>
              <td>{p.fecha}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
