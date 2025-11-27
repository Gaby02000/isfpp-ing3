import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Alert, Spinner } from 'react-bootstrap';

const ModalCrearComandaReserva = ({ show, onHide, reserva, mozos = [], productos = [], onConfirm }) => {
  const [formData, setFormData] = useState({
    id_mozo: '',
    observaciones: '',
    productos: []
  });

  const [detalleProductos, setDetalleProductos] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (show) {
      setFormData({
        id_mozo: '',
        observaciones: '',
        productos: []
      });
      setDetalleProductos([]);
      setError(null);
    }
  }, [show]);

  const handleMozoChange = (e) => {
    setFormData({
      ...formData,
      id_mozo: parseInt(e.target.value) || ''
    });
  };

  const handleObservacionesChange = (e) => {
    setFormData({
      ...formData,
      observaciones: e.target.value
    });
  };

  const handleAgregarProducto = (e) => {
    e.preventDefault();
    const idProducto = parseInt(e.target.id_producto.value);
    const cantidad = parseInt(e.target.cantidad.value);
    const producto = productos.find(p => p.id_producto === idProducto);

    if (!producto) {
      setError('Producto no válido');
      return;
    }

    if (cantidad <= 0) {
      setError('Cantidad debe ser mayor a 0');
      return;
    }

    const productoExistente = detalleProductos.find(d => d.id_producto === idProducto);
    if (productoExistente) {
      setError('Este producto ya está agregado');
      return;
    }

    const nuevoDetalle = {
      id_producto: idProducto,
      cantidad: cantidad,
      nombre: producto.nombre,
      precio_unitario: producto.precio,
      subtotal: cantidad * producto.precio
    };

    setDetalleProductos([...detalleProductos, nuevoDetalle]);
    setError(null);
    e.target.reset();
  };

  const handleRemoverProducto = (idProducto) => {
    setDetalleProductos(detalleProductos.filter(p => p.id_producto !== idProducto));
  };

  const handleConfirm = async () => {
    if (!formData.id_mozo) {
      setError('Debes seleccionar un mozo');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        id_reserva: reserva.id_reserva,
        id_mozo: formData.id_mozo,
        observaciones: formData.observaciones || undefined,
        productos: detalleProductos.map(d => ({
          id_producto: d.id_producto,
          cantidad: d.cantidad
        }))
      };

      await onConfirm(payload);
      onHide();
    } catch (err) {
      setError(err.message || 'Error al crear la comanda');
    } finally {
      setLoading(false);
    }
  };

  if (!reserva) return null;

  const totalComanda = detalleProductos.reduce((sum, p) => sum + p.subtotal, 0);

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>Crear Comanda desde Reserva #{reserva.numero}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

        <div className="mb-4 p-3 bg-light rounded">
          <h6>Información de la Reserva</h6>
          <p className="mb-1"><strong>Cliente:</strong> {reserva.cliente?.nombre} {reserva.cliente?.apellido}</p>
          <p className="mb-1"><strong>Mesa:</strong> {reserva.mesa?.numero} ({reserva.mesa?.tipo})</p>
          <p className="mb-0"><strong>Personas:</strong> {reserva.cant_personas}</p>
        </div>

        {/* Seleccionar Mozo */}
        <Form.Group className="mb-3">
          <Form.Label>Mozo *</Form.Label>
          <Form.Select value={formData.id_mozo} onChange={handleMozoChange} disabled={loading}>
            <option value="">-- Selecciona un mozo --</option>
            {mozos.map(m => (
              <option key={m.id} value={m.id}>
                {m.nombre_apellido || m.nombre}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        {/* Observaciones */}
        <Form.Group className="mb-3">
          <Form.Label>Observaciones (opcional)</Form.Label>
          <Form.Control
            as="textarea"
            rows={2}
            placeholder="Ej: Sin picante, sin cebolla, etc."
            value={formData.observaciones}
            onChange={handleObservacionesChange}
            disabled={loading}
          />
        </Form.Group>

        {/* Agregar Productos */}
        <Form.Group className="mb-3 p-3 bg-light rounded">
          <h6>Agregar Productos</h6>
          <Form onSubmit={handleAgregarProducto} className="d-flex gap-2">
            <Form.Select name="id_producto" required disabled={loading} style={{ flex: 1 }}>
              <option value="">-- Selecciona producto --</option>
              {productos.filter(p => !p.baja).map(p => (
                <option key={p.id_producto} value={p.id_producto}>
                  {p.nombre} (${p.precio.toFixed(2)})
                </option>
              ))}
            </Form.Select>
            <Form.Control
              type="number"
              name="cantidad"
              min="1"
              placeholder="Cant."
              required
              disabled={loading}
              style={{ width: '80px' }}
            />
            <Button type="submit" variant="primary" disabled={loading}>
              {loading ? <Spinner size="sm" /> : '+'} Agregar
            </Button>
          </Form>
        </Form.Group>

        {/* Tabla de Productos Agregados */}
        {detalleProductos.length > 0 && (
          <div className="mb-3">
            <h6>Productos en la Comanda</h6>
            <table className="table table-sm table-bordered">
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Cantidad</th>
                  <th>Precio</th>
                  <th>Subtotal</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {detalleProductos.map(p => (
                  <tr key={p.id_producto}>
                    <td>{p.nombre}</td>
                    <td>{p.cantidad}</td>
                    <td>${p.precio_unitario.toFixed(2)}</td>
                    <td>${p.subtotal.toFixed(2)}</td>
                    <td>
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleRemoverProducto(p.id_producto)}
                        disabled={loading}
                      >
                        ✕
                      </Button>
                    </td>
                  </tr>
                ))}
                <tr className="table-info">
                  <td colSpan="3" className="text-end"><strong>Total:</strong></td>
                  <td><strong>${totalComanda.toFixed(2)}</strong></td>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

        {detalleProductos.length === 0 && (
          <Alert variant="info" className="text-center">
            No hay productos agregados aún
          </Alert>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide} disabled={loading}>
          Cancelar
        </Button>
        <Button
          variant="success"
          onClick={handleConfirm}
          disabled={loading || !formData.id_mozo}
        >
          {loading ? <Spinner size="sm" className="me-2" /> : null}
          Crear Comanda
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalCrearComandaReserva;
