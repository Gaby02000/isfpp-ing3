import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaMozo = ({
  show,
  onHide,
  mozo,
  onConfirm
}) => {
  if (!mozo) return null;

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Confirmar Baja</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        ¿Está seguro que desea dar de baja al mozo <strong>{mozo.nombre_apellido}</strong>?
        <p className="text-muted mt-2">
          DNI: {mozo.documento} | Teléfono: {mozo.telefono}
        </p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cancelar
        </Button>
        <Button variant="danger" onClick={onConfirm}>
          Confirmar Baja
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalBajaMozo;