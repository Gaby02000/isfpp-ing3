import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaSecciones = ({ secciones, onEdit, onDelete }) => {
  if (secciones.length === 0) {
    return (
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan="3" className="text-center text-muted">
              No hay secciones registradas
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
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {secciones.map((seccion) => (
          <tr key={seccion.id_seccion}>
            <td>{seccion.nombre}</td>

            {/* Estado */}
            <td>
              <Badge bg={seccion.baja ? 'danger' : 'success'}>
                {seccion.baja ? 'Inactiva' : 'Activa'}
              </Badge>
            </td>

            {/* Acciones */}
            <td>
              <Button
                variant="warning"
                size="sm"
                className="me-2"
                onClick={() => onEdit(seccion)}
                disabled={seccion.baja}
              >
                Editar
              </Button>

              <Button
                variant="danger"
                size="sm"
                onClick={() => onDelete(seccion)}
                disabled={seccion.baja}
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

export default TablaSecciones;
