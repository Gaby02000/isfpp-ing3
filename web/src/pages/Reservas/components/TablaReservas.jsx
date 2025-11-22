import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaReservas = ({ reservas, clientes = [], mesas = [], onEdit, onCancel, onView }) => {

  const getClienteLabel = (id_cliente) => {
  const cliente = clientes.find(c => c.id_cliente === id_cliente);
  return cliente ? `${cliente.nombre} ${cliente.apellido}` : '-';
};

  const getMesaLabel = (id_mesa) => {
    const mesa = mesas.find(m => m.id_mesa === id_mesa);
    return mesa ? `Mesa ${mesa.numero} (${mesa.tipo})` : '-';
  };

  if (reservas.length === 0) {
    return (
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Número</th>
            <th>Cliente</th>
            <th>Mesa</th>
            <th>Fecha/Hora</th>
            <th>Personas</th>
            <th>cancelado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan="7" className="text-center text-muted">
              No hay reservas registradas
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
          <th>Cliente</th>
          <th>Mesa</th>
          <th>Fecha/Hora</th>
          <th>Personas</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {reservas.map((reserva) => (
          <tr key={reserva.id_reserva}>
            <td>{reserva.numero}</td>
            <td>
              {reserva.id_cliente ? (
                <Badge bg="info">{getClienteLabel(reserva.id_cliente)}</Badge>
              ) : (
                <span className="text-muted">-</span>
              )}
            </td>
            <td>
              {reserva.id_mesa ? (
                <Badge bg="secondary">{getMesaLabel(reserva.id_mesa)}</Badge>
              ) : (
                <span className="text-muted">-</span>
              )}
            </td>
            <td>{new Date(reserva.fecha_hora).toLocaleString()}</td>
            <td>{reserva.cant_personas}</td>

            {/* Estado */}
            <td>
              {(() => {
                // Preferir estado derivado desde backend si viene
                const estado = reserva.estado || (reserva.cancelado ? (reserva.motivo_cancelacion === 'ausencia' ? 'por ausencia' : 'cancelada') : 'activa');
                if (estado === 'activa') return <Badge bg="success">Activa</Badge>;
                if (estado === 'por ausencia') return <Badge bg="secondary">Por ausencia</Badge>;
                return <Badge bg="danger">Cancelada</Badge>;
              })()}
            </td>

            {/* Acciones */}
            <td>
              <Button
                variant="info"
                size="sm"
                className="me-2"
                onClick={() => onView && onView(reserva)}
              >
                Ver
              </Button>

              <Button
                variant="warning"
                size="sm"
                className="me-2"
                onClick={() => onEdit(reserva)}
                disabled={reserva.cancelado}
              >
                Editar
              </Button>

              <Button
                variant="danger"
                size="sm"
                onClick={() => onCancel(reserva)}
                disabled={reserva.cancelado}
              >
                Cancelar
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default TablaReservas;