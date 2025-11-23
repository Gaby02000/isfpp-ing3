import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col, Table, Badge } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik, FieldArray } from 'formik';
import { comandaValidationSchema } from '../../../utils/validations';


const ModalComanda = ({ 
  show, 
  onHide,
  editingComanda,
  onSubmit,
  mesas,
  mozos,
  productos,
}) => {

  const calcularTotal = (productosSeleccionados) => {
    return productosSeleccionados.reduce((total, item) => {
      const producto = productos.find(p => p.id_producto === parseInt(item.id_producto));
      if (producto) {
        return total + (parseFloat(producto.precio) * parseInt(item.cantidad));
      }
      return total;
    }, 0);
  };

  return (
    <Modal show={show} onHide={onHide} size="xl">
      <Formik
        initialValues={{
          fecha: editingComanda?.fecha || new Date().toISOString().split('T')[0],
          id_mesa: editingComanda?.id_mesa || '',
          id_mozo: editingComanda?.id_mozo || '',
          observaciones: editingComanda?.observaciones || '',
          productos: editingComanda?.detalles?.map(d => ({
            id_producto: d.id_producto,
            cantidad: d.cantidad
          })) || []
        }}
        validationSchema={comandaValidationSchema}
        onSubmit={onSubmit}
        enableReinitialize
      >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting, setFieldValue }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
              <Modal.Title>
                {editingComanda ? 'Modificar Comanda' : 'Nueva Comanda'}
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              {/* Datos básicos */}
              <Row className="mb-4">
                <Col md={4}>
                  <CampoFormulario
                    label="Fecha"
                    name="fecha"
                    type="date"
                    value={values.fecha}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.fecha}
                    error={errors.fecha}
                  />
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Mesa *</Form.Label>
                    <Form.Select
                      name="id_mesa"
                      value={values.id_mesa}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      isInvalid={touched.id_mesa && errors.id_mesa}
                    >
                      <option value="">Seleccione una mesa</option>
                      {mesas
                        .filter(mesa => !mesa.baja)
                        .map((mesa) => (
                          <option key={mesa.id_mesa} value={mesa.id_mesa}>
                            Mesa {mesa.numero} ({mesa.cant_comensales} personas)
                          </option>   
                        ))}
                    </Form.Select>
                    <Form.Control.Feedback type="invalid">
                      {errors.id_mesa}
                    </Form.Control.Feedback>
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Mozo *</Form.Label>
                    <Form.Select
                      name="id_mozo"
                      value={values.id_mozo}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      isInvalid={touched.id_mozo && errors.id_mozo}
                    >
                      <option value="">Seleccione un mozo</option>
                      {mozos
                        .filter(mozo => !mozo.baja)
                        .map((mozo) => (
                          <option key={mozo.id} value={mozo.id}>
                            {mozo.nombre_apellido}
                          </option>
                        ))}
                    </Form.Select>
                    <Form.Control.Feedback type="invalid">
                      {errors.id_mozo}
                    </Form.Control.Feedback>
                  </Form.Group>
                </Col>
              </Row>

              {/* Productos */}
              <div className="mb-3">
                <h5>Productos de la Comanda</h5>
                <FieldArray name="productos">
                  {({ push, remove }) => (
                    <>
                      <Table striped bordered hover size="sm">
                        <thead>
                          <tr>
                            <th>Producto</th>
                            <th style={{width: '120px'}}>Cantidad</th>
                            <th style={{width: '120px'}}>Precio Unit.</th>
                            <th style={{width: '120px'}}>Subtotal</th>
                            <th style={{width: '80px'}}>Acción</th>
                          </tr>
                        </thead>
                        <tbody>
                          {values.productos.length === 0 ? (
                            <tr>
                              <td colSpan="5" className="text-center text-muted">
                                No hay productos agregados
                              </td>
                            </tr>
                          ) : (
                            values.productos.map((producto, index) => {
                              const productoData = productos.find(p => p.id_producto === parseInt(producto.id_producto));
                              const subtotal = productoData ? parseFloat(productoData.precio) * parseInt(producto.cantidad || 0) : 0;
                              
                              return (
                                <tr key={index}>
                                  <td>
                                    {productoData ? productoData.nombre : '-'}
                                  </td>
                                  <td>
                                    <Form.Control
                                      type="number"
                                      min="1"
                                      value={producto.cantidad}
                                      onChange={(e) => setFieldValue(`productos.${index}.cantidad`, e.target.value)}
                                      size="sm"
                                    />
                                  </td>
                                  <td className="text-end">
                                    ${productoData ? parseFloat(productoData.precio).toFixed(2) : '0.00'}
                                  </td>
                                  <td className="text-end">
                                    <strong>${subtotal.toFixed(2)}</strong>
                                  </td>
                                  <td className="text-center">
                                    <Button
                                      variant="danger"
                                      size="sm"
                                      onClick={() => remove(index)}
                                    >
                                      ✕
                                    </Button>
                                  </td>
                                </tr>
                              );
                            })
                          )}
                          <tr className="table-secondary">
                            <td colSpan="3" className="text-end"><strong>TOTAL:</strong></td>
                            <td className="text-end">
                              <strong>${calcularTotal(values.productos).toFixed(2)}</strong>
                            </td>
                            <td></td>
                          </tr>
                        </tbody>
                      </Table>

                      {/* Agregar producto */}
                      <Row>
                        <Col md={10}>
                          <Form.Select
                            id="nuevoProducto"
                            onChange={(e) => {
                              if (e.target.value) {
                                // Verificar si ya existe
                                const existe = values.productos.some(p => p.id_producto === e.target.value);
                                if (!existe) {
                                  push({ id_producto: e.target.value, cantidad: 1 });
                                }
                                e.target.value = '';
                              }
                            }}
                          >
                            <option value="">➕ Agregar producto...</option>
                            {productos
                              .filter(p => !values.productos.some(vp => vp.id_producto === p.id_producto.toString()))
                              .map((producto) => (
                                <option key={producto.id_producto} value={producto.id_producto}>
                                  {producto.nombre} - ${parseFloat(producto.precio).toFixed(2)}
                                </option>
                              ))}
                          </Form.Select>
                        </Col>
                      </Row>
                    </>
                  )}
                </FieldArray>
              </div>

              {/* Observaciones */}
              <Row>
                <Col md={12}>
                  <Form.Group className="mb-3">
                    <Form.Label>Observaciones</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={2}
                      name="observaciones"
                      value={values.observaciones}
                      onChange={handleChange}
                      placeholder="Observaciones adicionales..."
                    />
                  </Form.Group>
                </Col>
              </Row>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
              </Button>
              <Button variant="primary" type="submit" disabled={isSubmitting}>
                {editingComanda ? 'Guardar Cambios' : 'Crear Comanda'}
              </Button>
            </Modal.Footer>
          </Form>
        )}  
      </Formik>
    </Modal>
  );
};

export default ModalComanda;