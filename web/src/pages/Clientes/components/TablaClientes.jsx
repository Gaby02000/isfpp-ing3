import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaClientes = ({ clientes, onEdit, onDelete }) => {
  // 1. Manejar el estado vacío para 'clientes'
  if (clientes.length === 0) {
    return (
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            {/* 2. Actualizar las columnas de la cabecera */}
            <th>Documento</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            {/* 3. Ajustar el colSpan y el mensaje */}
            <td colSpan="7" className="text-center text-muted">
              No hay clientes registrados
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
          {/* 2. (Repetir) Actualizar las columnas de la cabecera */}
          <th>Documento</th>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Teléfono</th>
          <th>Email</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {/* 4. Mapear sobre 'clientes' */}
        {clientes.map((cliente) => (
          // 5. Usar 'id_cliente' como key
          <tr key={cliente.id_cliente}>
            {/* 6. Mostrar los datos del cliente */}
            <td>{cliente.documento}</td>
            <td>{cliente.nombre}</td>
            <td>{cliente.apellido}</td>
            <td>{cliente.num_telefono}</td>
            <td>{cliente.email}</td>
            <td>
              {/* 7. Adaptar el Badge para 'cliente.baja' */}
              <Badge bg={cliente.baja ? 'danger' : 'success'}>
                {cliente.baja ? 'Inactivo' : 'Activo'}
              </Badge>
            </td>
            <td>
              {/* 8. Pasar el objeto 'cliente' a las funciones */}
              <Button
                variant="warning"
                size="sm"
                className="me-2"
                onClick={() => onEdit(cliente)}
                disabled={cliente.baja} // Deshabilitar si está inactivo
              >
                Editar
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => onDelete(cliente)}
                disabled={cliente.baja} // Deshabilitar si ya está inactivo
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

export default TablaClientes;