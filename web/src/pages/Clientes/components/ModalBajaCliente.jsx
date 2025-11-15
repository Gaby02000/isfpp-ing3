import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ModalBajaCliente = ({ 
  show, 
  onHide, 
  cliente, // 1. Renombramos la prop
  onConfirm 
}) => {
  
  // 2. Verificamos el cliente
  if (!cliente) return null;

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Confirmar Baja</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {/* 3. Usamos el documento para identificar */}
        ¿Está seguro que desea dar de baja el cliente con documento <strong>{cliente.documento}</strong>?
        
        {/* 4. Mostramos información relevante del cliente */}
        <p className="text-muted mt-2">
          Nombre: {cliente.nombre} {cliente.apellido}
        </p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cancelar
        </Button>
        {/* Este botón llamará a 'onConfirm'. 
          El componente padre (la página) será el que tenga la lógica
          de llamar a deleteCliente(cliente.id_cliente)
        */}
        <Button variant="danger" onClick={onConfirm}>
          Confirmar Baja
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalBajaCliente;

