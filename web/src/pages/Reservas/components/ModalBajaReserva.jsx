import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const ModalBajaReserva = ({
  show,
  onHide,
  reserva,
  onConfirm
}) => {
  const [motivo, setMotivo] = useState('');
  const [seniaDevuelta, setSeniaDevuelta] = useState(false);

  if (!reserva) return null;

  const handleConfirm = () => {
    onConfirm({ motivo, senia_devuelta: seniaDevuelta });
  };

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

        <Form className="mt-3">
          <Form.Group className="mb-2">
            <Form.Label>Motivo de cancelación</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              placeholder="Indique el motivo de la cancelación"
              value={motivo}
              onChange={(e) => setMotivo(e.target.value)}
            />
          </Form.Group>

          <Form.Group>
            <Form.Check
              type="checkbox"
              label="Devolver seña"
              checked={seniaDevuelta}
              onChange={(e) => setSeniaDevuelta(e.target.checked)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Volver
        </Button>
        <Button variant="danger" onClick={handleConfirm} disabled={!motivo}>
          Confirmar Cancelación
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalBajaReserva;