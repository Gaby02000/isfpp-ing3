import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaMesa = ({ 
  show, 
  onHide, 
  mesa, 
  onConfirm 
}) => {
  if (!mesa) return null;

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Confirmar Baja</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        ¿Está seguro que desea dar de baja la mesa <strong>#{mesa.numero}</strong>?
        <p className="text-muted mt-2">
          Tipo: {mesa.tipo} | Comensales: {mesa.cant_comensales}
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

export default ModalBajaMesa;

