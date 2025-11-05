import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaMesas = ({ mesas, onEdit, onDelete }) => {
  if (mesas.length === 0) {
    return (
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Número</th>
            <th>Tipo</th>
            <th>Comensales</th>
            <th>Sector</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan="6" className="text-center text-muted">
              No hay mesas registradas
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
          <th>ID</th>
          <th>Número</th>
          <th>Tipo</th>
          <th>Comensales</th>
          <th>Sector</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {mesas.map((mesa) => (
          <tr key={mesa.id_mesa}>
            <td>{mesa.numero}</td>
            <td>{mesa.tipo}</td>
            <td>{mesa.cant_comensales}</td>
            <td>
              {mesa.sector ? (
                <Badge bg="info">Sector {mesa.sector.numero}</Badge>
              ) : (
                <span className="text-muted">-</span>
              )}
            </td>
            <td>
              <Badge bg={mesa.baja ? 'danger' : 'success'}>
                {mesa.baja ? 'Inactiva' : 'Activa'}
              </Badge>
            </td>
            <td>
              <Button
                variant="warning"
                size="sm"
                className="me-2"
                onClick={() => onEdit(mesa)}
                disabled={mesa.baja}
              >
                Editar
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => onDelete(mesa)}
                disabled={mesa.baja}
              >
                Baja
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default TablaMesas;

