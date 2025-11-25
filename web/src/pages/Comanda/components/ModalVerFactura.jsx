import React from 'react';
import { Modal, Button, Table, Row, Col, Badge } from 'react-bootstrap';

const ModalVerFactura = ({ show, onHide, factura }) => {
  if (!factura) return null;

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton className="bg-success text-white">
        <Modal.Title>✅ Factura Generada Exitosamente</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {/* Encabezado de la factura */}
        <div className="text-center mb-4 p-3 bg-light rounded">
          <h3 className="mb-1">FACTURA</h3>
          <h5 className="text-primary">{factura.codigo}</h5>
          <p className="text-muted mb-0">Fecha: {new Date(factura.fecha).toLocaleString('es-AR')}</p>
        </div>

        {/* Información del cliente y comanda */}
        <Row className="mb-3">
          <Col md={6}>
            <div className="border rounded p-3">
              <h6 className="text-muted mb-2">DATOS DEL CLIENTE</h6>
              {factura.cliente ? (
                <>
                  <p className="mb-1"><strong>Nombre:</strong> {factura.cliente.nombre} {factura.cliente.apellido}</p>
                  <p className="mb-1"><strong>Documento:</strong> {factura.cliente.documento}</p>
                  <p className="mb-1"><strong>Email:</strong> {factura.cliente.email}</p>
                  <p className="mb-0"><strong>Teléfono:</strong> {factura.cliente.num_telefono}</p>
                </>
              ) : (
                <p className="text-muted mb-0">Consumidor Final</p>
              )}
            </div>
          </Col>
          <Col md={6}>
            <div className="border rounded p-3">
              <h6 className="text-muted mb-2">DATOS DE LA COMANDA</h6>
              <p className="mb-1"><strong>Comanda N°:</strong> #{factura.id_comanda}</p>
              {factura.comanda && (
                <>
                  <p className="mb-1"><strong>Mesa:</strong> {factura.comanda.mesa?.numero || '-'}</p>
                  <p className="mb-1"><strong>Mozo:</strong> {factura.comanda.mozo?.nombre_apellido || '-'}</p>
                  <p className="mb-0">
                    <strong>Estado:</strong> <Badge bg="secondary">Cerrada</Badge>
                  </p>
                </>
              )}
            </div>
          </Col>
        </Row>

        {/* Detalle de productos */}
        <h6 className="mb-3">DETALLE DE PRODUCTOS</h6>
        <Table bordered hover>
          <thead className="table-light">
            <tr>
              <th>Producto</th>
              <th className="text-center" style={{width: '100px'}}>Cantidad</th>
              <th className="text-end" style={{width: '120px'}}>Precio Unit.</th>
              <th className="text-end" style={{width: '120px'}}>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {factura.detalles && factura.detalles.length > 0 ? (
              factura.detalles.map((detalle, index) => (
                <tr key={index}>
                  <td>{detalle.producto?.nombre || 'Producto'}</td>
                  <td className="text-center">{detalle.cantidad}</td>
                  <td className="text-end">${parseFloat(detalle.precio_unitario).toFixed(2)}</td>
                  <td className="text-end"><strong>${parseFloat(detalle.subtotal).toFixed(2)}</strong></td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="text-center text-muted">Sin productos</td>
              </tr>
            )}
          </tbody>
          <tfoot className="table-secondary">
            <tr>
              <td colSpan="3" className="text-end"><strong>TOTAL:</strong></td>
              <td className="text-end">
                <h5 className="mb-0 text-success">${parseFloat(factura.total).toFixed(2)}</h5>
              </td>
            </tr>
          </tfoot>
        </Table>

        {/* Mensaje de éxito */}
        <div className="alert alert-success mt-3">
          <strong>✅ La factura se ha generado correctamente.</strong>
          <br />
          La comanda #{factura.id_comanda} ha sido cerrada.
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="outline-secondary" onClick={onHide}>
          Cerrar
        </Button>
        <Button variant="primary" onClick={() => window.print()}>
          🖨️ Imprimir Factura
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalVerFactura;