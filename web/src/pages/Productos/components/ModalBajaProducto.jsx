import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaProducto = ({
  show,
  onHide,
  producto,
  onConfirm
}) => {
  if (!producto) return null;

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Confirmar Baja de Producto</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        ¿Está seguro que desea dar de baja el producto <strong>{producto.nombre}</strong>?
        <p className="text-muted mt-2">
          Código: {producto.codigo} <br />
          Precio: ${producto.precio.toFixed(2)} <br />
          Sección ID: {producto.id_seccion}
        </p>
        {producto.descripcion && (
          <p className="text-secondary mt-2">
            <em>"{producto.descripcion}"</em>
          </p>
        )}
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

export default ModalBajaProducto;
