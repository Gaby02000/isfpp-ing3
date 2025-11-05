import React from 'react';
import { Modal, Button, Alert } from 'react-bootstrap';

const ModalBajaSector = ({ 
  show, 
  onHide, 
  sector, 
  onConfirm 
}) => {
  if (!sector) return null;

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Confirmar Baja</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        ¿Está seguro que desea dar de baja el sector <strong>#{sector.numero}</strong>?
        {sector.cantidad_mesas > 0 && (
          <Alert variant="warning" className="mt-2">
            Este sector tiene {sector.cantidad_mesas} mesa(s) activa(s). 
            Primero debe reasignar o dar de baja las mesas.
          </Alert>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cancelar
        </Button>
        <Button 
          variant="danger" 
          onClick={onConfirm}
          disabled={sector.cantidad_mesas > 0}
        >
          Confirmar Baja
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalBajaSector;

