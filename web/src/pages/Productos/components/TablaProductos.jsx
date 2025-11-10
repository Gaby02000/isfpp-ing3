import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaProducto = ({ productos, secciones = [], onEdit, onDelete }) => {

  const getSeccionLabel = (id_seccion) => {
    const seccion = secciones.find(s => s.id_seccion === id_seccion);
    return seccion ? seccion.nombre : '-';
  };

  if (productos.length === 0) {
    return (
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Sección</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan="6" className="text-center text-muted">
              No hay productos registrados
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
          <th>Código</th>
          <th>Nombre</th>
          <th>Precio</th>
          <th>Sección</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {productos.map((producto) => (
          <tr key={producto.id_producto}>
            <td>{producto.codigo}</td>
            <td>{producto.nombre}</td>
            <td>${Number(producto.precio).toFixed(2)}</td>

            {/* Sección */}
            <td>
              {producto.id_seccion ? (
                <Badge bg="info">{getSeccionLabel(producto.id_seccion)}</Badge>
              ) : (
                <span className="text-muted">-</span>
              )}
            </td>

            {/* Estado */}
            <td>
              <Badge bg={producto.baja ? 'danger' : 'success'}>
                {producto.baja ? 'Inactivo' : 'Activo'}
              </Badge>
            </td>

            {/* Acciones */}
            <td>
              <Button
                variant="warning"
                size="sm"
                className="me-2"
                onClick={() => onEdit(producto)}
                disabled={producto.baja}
              >
                Editar
              </Button>

              <Button
                variant="danger"
                size="sm"
                onClick={() => onDelete(producto)}
                disabled={producto.baja}
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

export default TablaProducto;
