import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaMedioPagos = ({ medioPagos, onEdit, onDelete }) => {
  if (medioPagos.length === 0) {
    return (
        <Table striped bordered hover responsive>
        <thead>
            <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td colSpan="4" className="text-center text-muted">
                No hay medios de pago registrados
            </td>
            </tr>
        </tbody>
        </Table>
    );
  }
    return (    
    <Table striped bordered hover responsive>
      <thead>
        <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
        </tr>
        </thead>
        <tbody>
        {medioPagos.map((medioPago) => (
            <tr key={medioPago.id_medio_pago}>
            <td>{medioPago.nombre}</td>
            <td>{medioPago.descripcion || <span className="text-muted">-</span>}</td>
            <td>
                <Badge bg={medioPago.baja ? 'danger' : 'success'}>
                {medioPago.baja ? 'Inactivo' : 'Activo'}
                </Badge>
            </td>
            <td>
                <Button
                variant="primary"
                size="sm"
                className="me-2"
                onClick={() => onEdit(medioPago)}
                >
                Editar
                </Button>
                <Button
                variant="danger"
                size="sm"
                onClick={() => onDelete(medioPago)}
                >
                Eliminar
                </Button>
            </td>
            </tr>   
        ))}
        </tbody>
    </Table>
    );
}
export default TablaMedioPagos;