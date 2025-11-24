import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaComandas = ({ comandas, onEdit, onDelete, onGenerarFactura, onVerFactura }) => {
  if (comandas.length === 0) {
    return (    
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Número de Comanda</th>
            <th>Número de Mesa</th>
            <th>Mozo</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>    
        <tbody>
          <tr>
            <td colSpan="5" className="text-center text-muted">
              No hay comandas registradas
            </td>
          </tr>
        </tbody>
      </Table>
    );
  }

  const getEstadoBadge = (estado) => {
    switch(estado) {
      case 'Abierta':
        return <Badge bg="success">Abierta</Badge>;
      case 'Cerrada':
        return <Badge bg="secondary">Cerrada</Badge>;
      case 'Cancelada':
        return <Badge bg="danger">Cancelada</Badge>;
      default:
        return <Badge bg="warning">Desconocido</Badge>;
    }
  };

  return (
    <Table striped bordered hover responsive>
      <thead>
        <tr>
          <th style={{width: '120px'}}>N° Comanda</th>
          <th style={{width: '120px'}}>N° Mesa</th>
          <th style={{width: '180px'}}>Mozo</th>
          <th style={{width: '100px'}}>Estado</th>
          <th style={{width: '120px'}}>Total</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {comandas.map((comanda) => (
          <tr key={comanda.id_comanda}>
            <td>
              <Badge bg="info">#{comanda.id_comanda}</Badge>
            </td>
            <td>
              {comanda.mesa ? (
                <Badge bg="info">Mesa {comanda.mesa.numero}</Badge>
              ) : (
                <span className="text-muted">-</span>
              )}
            </td>
            <td>
              {comanda.mozo ? (
                <span>{comanda.mozo.nombre_apellido}</span>
              ) : (   
                <span className="text-muted">Sin mozo</span>
              )}
            </td>
            <td>
              {getEstadoBadge(comanda.estado)}
            </td>
            <td className="text-end">
              <strong>${parseFloat(comanda.total || 0).toFixed(2)}</strong>
            </td>
            <td>
              <div className="d-flex gap-1 flex-wrap">
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => onEdit(comanda)}
                  disabled={comanda.estado !== 'Abierta' || comanda.baja}
                  title="Editar comanda"
                >
                  ✏️ Editar
                </Button>
                
                {comanda.estado === 'Abierta' && !comanda.baja && (
                  <Button
                    variant="success"
                    size="sm"
                    onClick={() => onGenerarFactura(comanda)}
                    disabled={!comanda.detalles || comanda.detalles.length === 0}
                    title="Generar factura"
                  >
                    🧾 Facturar
                  </Button>
                )}
                {comanda.estado === 'Cerrada' && ( 
                  <Button
                   variant="info"
                  size="sm"
                  onClick={() => onVerFactura(comanda)} // <-- Llama a la nueva función con el objeto comanda
                  title="Ver Factura"
                  >
                  📄 Ver Factura
                  </Button>
                )}
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => onDelete(comanda)}
                  disabled={comanda.baja || comanda.estado === 'Cerrada'}
                  title="Dar de baja"
                >
                  🗑️ Baja
                </Button>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default TablaComandas;