import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaComanda = ({
    show,
    onHide,
    comanda,
    onConfirm
}) => {
    if (!comanda) return null;  

    return (
        <Modal show={show} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>Confirmar Baja</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                ¿Está seguro que desea dar de baja la comanda <strong>#{comanda.id_comanda}</strong>?
                <p className="text-muted mt-2">
                    Mesa: {comanda.mesa_numero} | Mozo: {comanda.mozo_nombre}
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

export default ModalBajaComanda;
