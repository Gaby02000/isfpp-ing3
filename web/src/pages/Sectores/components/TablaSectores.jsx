import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaSectores = ({ sectores, onEdit, onDelete }) => {
  if (sectores.length === 0) {
    return (
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Número</th>
            <th>Cantidad de Mesas</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan="4" className="text-center text-muted">
              No hay sectores registrados
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
            <th>Número</th>
            <th>Cantidad de Mesas</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {sectores.map((sector) => (
            <tr key={sector.id_sector}>
              <td>{sector.numero}</td>
              <td>{sector.cantidad_mesas || 0}</td>
              <td>
                <Badge bg={sector.baja ? 'danger' : 'success'}>
                  {sector.baja ? 'Inactivo' : 'Activo'}
                </Badge>
              </td>
              <td>
                <Button
                  variant="warning"
                  size="sm"
                  className="me-2"
                  onClick={() => onEdit(sector)}
                  disabled={sector.baja}
                >
                  Editar
                </Button>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => onDelete(sector)}
                  disabled={sector.baja}
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

export default TablaSectores;

