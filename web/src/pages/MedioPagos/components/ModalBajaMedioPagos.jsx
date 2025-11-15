import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaMedioPagos = ({ 
  show, 
  onHide,
    medioPago,
    onConfirm
}) => {
  if (!medioPago) return null;

    return (
        <Modal show={show} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>Confirmar Baja</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                ¿Está seguro que desea dar de baja el medio de pago <strong>{medioPago.nombre}</strong>?
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
}
export default ModalBajaMedioPagos;