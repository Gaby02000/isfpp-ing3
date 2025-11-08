import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaMozos = ({ mozos, sectores = [] , onEdit, onDelete }) => {
  const getSectorLabel = (id_sector) => {
    const sector = sectores.find(s => s.id_sector === id_sector);
    return sector ? `Sector ${sector.numero}` : '-';
  };

  if (mozos.length === 0) {
    return (
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>DNI</th>
            <th>Teléfono</th>
            <th>Domicilio</th>
            <th>Sector</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan="6" className="text-center text-muted">
              No hay mozos registrados
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
          <th>DNI</th>
          <th>Teléfono</th>
            <th>Domicilio</th>
          <th>Sector</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {mozos.map((mozo) => (
          <tr key={mozo.id}>
            <td>{mozo.nombre_apellido}</td>
            <td>{mozo.documento}</td>
            <td>{mozo.telefono}</td>
            <td>{mozo.direccion}</td>
            <td>
              {mozo.id_sector ? (
                <Badge bg="info">{getSectorLabel(mozo.id_sector)}</Badge>
              ) : (
                <span className="text-muted">-</span>
              )}
            </td>
            <td>
              <Badge bg={mozo.baja ? 'danger' : 'success'}>
                {mozo.baja ? 'Inactivo' : 'Activo'}
              </Badge>
            </td>
            <td>
              <Button
                variant="warning"
                size="sm"
                className="me-2"
                onClick={() => onEdit(mozo)}
                disabled={mozo.baja}
              >
                Editar
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => onDelete(mozo)}
                disabled={mozo.baja}
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

export default TablaMozos;