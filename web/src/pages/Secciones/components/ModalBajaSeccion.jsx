import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaSeccion = ({ show, onHide, seccion, onConfirm }) => {
  if (!seccion) return null;

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Confirmar Baja de Sección</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        ¿Está seguro que desea dar de baja la sección <strong>{seccion.nombre}</strong>?
        <p className="text-muted mt-2">
          ID: {seccion.id_seccion}
        </p>
        {seccion.descripcion && (
          <p className="text-secondary mt-2">
            <em>"{seccion.descripcion}"</em>
          </p>
        )}
        <p className="text-danger fw-bold mt-3 mb-0">
          ⚠️ Esta acción desactivará la sección y podría afectar los productos asociados.
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

export default ModalBajaSeccion;
