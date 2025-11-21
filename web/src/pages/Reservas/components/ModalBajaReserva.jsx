import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaReserva = ({
  show,
  onHide,
  reserva,
  onConfirm
}) => {
  if (!reserva) return null;

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Confirmar Cancelación de Reserva</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        ¿Está seguro que desea cancelar la reserva <strong>#{reserva.numero}</strong>?
        <p className="text-muted mt-2">
          Cliente ID: {reserva.id_cliente} <br />
          Mesa ID: {reserva.id_mesa} <br />
          Fecha y hora: {new Date(reserva.fecha_hora).toLocaleString()} <br />
          Cantidad de personas: {reserva.cant_personas}
        </p>
        {reserva.cancelado && (
          <p className="text-secondary mt-2">
            <em>⚠️ Esta reserva ya está cancelada</em>
          </p>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Volver
        </Button>
        <Button variant="danger" onClick={onConfirm}>
          Confirmar Cancelación
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalBajaReserva;