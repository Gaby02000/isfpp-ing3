import React, { useState, useEffect } from 'react';
import { Modal, Button, Table, Badge, Form } from 'react-bootstrap';

const ModalGenerarFactura = ({
  show,
  onHide,
  comanda,
  onConfirm,
  loading,
  clientes
}) => {
  const [idClienteSeleccionado, setIdClienteSeleccionado] = useState('');

  useEffect(() => {
    // Si la comanda ya tiene cliente, pre-seleccionarlo
    if (comanda?.id_cliente) {
      setIdClienteSeleccionado(comanda.id_cliente);
    } else {
      setIdClienteSeleccionado(''); // Reset cuando cambia la comanda
    }
  }, [comanda]);

  if (!comanda) return null;

  const calcularTotal = () => {
    if (!comanda.detalles || comanda.detalles.length === 0) return 0;
    return comanda.detalles.reduce((total, detalle) => {
      return total + (parseFloat(detalle.precio_unitario) * parseInt(detalle.cantidad));
    }, 0);
  };

  const total = calcularTotal();

  const handleConfirmar = () => {
    // Pasar el id_cliente seleccionado a la función de confirmación
    onConfirm(idClienteSeleccionado || null);
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>🧾 Generar Factura</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div className="mb-3">
          <h5>Resumen de la Comanda #{comanda.id_comanda}</h5>
          <p className="text-muted mb-3">
            <strong>Mesa:</strong> {comanda.mesa?.numero || '-'} | 
            <strong> Mozo:</strong> {comanda.mozo?.nombre_apellido || '-'} | 
            <strong> Fecha:</strong> {comanda.fecha}
          </p>
        </div>

        {/* SELECTOR DE CLIENTE */}
        <div className="mb-4 p-3 border rounded bg-light">
          <Form.Group>
            <Form.Label className="fw-bold">
              Cliente para la factura <span className="text-danger">*</span>
            </Form.Label>
            <Form.Select
              value={idClienteSeleccionado}
              onChange={(e) => setIdClienteSeleccionado(e.target.value)}
              required
            >
              <option value="">-- Seleccione un cliente --</option>
              {clientes && clientes
                .filter(cliente => !cliente.baja)
                .map((cliente) => (
                  <option key={cliente.id_cliente} value={cliente.id_cliente}>
                    {cliente.nombre} {cliente.apellido} - {cliente.documento}
                  </option>
                ))}
            </Form.Select>
            <Form.Text className="text-muted">
              💡 Si el cliente no existe, primero debes registrarlo en "Gestión de Clientes"
            </Form.Text>
          </Form.Group>
        </div>

        <Table bordered hover size="sm">
          <thead>
            <tr>
              <th>Producto</th>
              <th style={{width: '100px'}} className="text-center">Cant.</th>
              <th style={{width: '120px'}} className="text-end">Precio Unit.</th>
              <th style={{width: '120px'}} className="text-end">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {comanda.detalles && comanda.detalles.length > 0 ? (
              comanda.detalles.map((detalle, index) => {
                const subtotal = parseFloat(detalle.precio_unitario) * parseInt(detalle.cantidad);
                return (
                  <tr key={index}>
                    <td>
                      {detalle.producto?.nombre || 'Producto sin nombre'}
                      {detalle.entregado && (
                        <Badge bg="success" className="ms-2">Entregado</Badge>
                      )}
                    </td>
                    <td className="text-center">{detalle.cantidad}</td>
                    <td className="text-end">${parseFloat(detalle.precio_unitario).toFixed(2)}</td>
                    <td className="text-end"><strong>${subtotal.toFixed(2)}</strong></td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="4" className="text-center text-muted">
                  No hay productos en esta comanda
                </td>
              </tr>
            )}
          </tbody>
          <tfoot>
            <tr className="table-secondary">
              <td colSpan="3" className="text-end"><strong>TOTAL:</strong></td>
              <td className="text-end">
                <h5 className="mb-0">${total.toFixed(2)}</h5>
              </td>
            </tr>
          </tfoot>
        </Table>

        <div className="alert alert-info mt-3">
          <strong>⚠️ Atención:</strong> Al generar la factura, la comanda se cerrará automáticamente y no podrá ser modificada.
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide} disabled={loading}>
          Cancelar
        </Button>
        <Button 
          variant="success" 
          onClick={handleConfirmar} 
          disabled={
            loading || 
            !idClienteSeleccionado || 
            !comanda.detalles || 
            comanda.detalles.length === 0
          }
        >
          {loading ? 'Generando...' : '🧾 Generar Factura'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalGenerarFactura;