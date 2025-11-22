import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalDetalleReserva = ({ show, onHide, reserva }) => {
  if (!reserva) return null;

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>Detalle Reserva #{reserva.numero}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p><strong>Cliente:</strong> {reserva.cliente?.nombre} {reserva.cliente?.apellido}</p>
        <p><strong>Mesa:</strong> {reserva.mesa?.numero} - {reserva.mesa?.tipo}</p>
        <p><strong>Fecha/Hora:</strong> {new Date(reserva.fecha_hora).toLocaleString()}</p>
        <p><strong>Personas:</strong> {reserva.cant_personas}</p>
        <p><strong>Estado:</strong> {reserva.estado || (reserva.cancelado ? 'Cancelada' : 'Activa')}</p>
        <p><strong>Motivo cancelación:</strong> {reserva.motivo_cancelacion || '-'}</p>
        <p><strong>Seña devuelta:</strong> {reserva.senia_devuelta ? 'Sí' : 'No'}</p>
        <p><strong>Seña recuperada:</strong> {reserva.senia_recuperada ? 'Sí' : 'No'}</p>
        <p><strong>Asistida:</strong> {reserva.asistida ? 'Sí' : 'No'}</p>
        <p><strong>Creada:</strong> {reserva.fecha_creacion}</p>
        <p><strong>Modificada:</strong> {reserva.fecha_modificacion}</p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>Cerrar</Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalDetalleReserva;
