import React from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik } from 'formik';
import { productoValidationSchema } from '../../../utils/validations';

const ModalProducto = ({
  show,
  onHide,
  editingProducto,
  onSubmit,
  secciones
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Formik
        initialValues={{
          codigo: editingProducto?.codigo || '',
          nombre: editingProducto?.nombre || '',
          precio: editingProducto?.precio || '',
          descripcion: editingProducto?.descripcion || '',
          id_seccion: editingProducto?.id_seccion || '',
        }}
        validationSchema={productoValidationSchema}
        onSubmit={(values, actions) => {
          console.log("Formik onSubmit ejecutado", values);
          onSubmit(values, actions);
        }}
      >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
              <Modal.Title>
                {editingProducto ? 'Modificar Producto' : 'Nuevo Producto'}
              </Modal.Title>
            </Modal.Header>

            <Modal.Body>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Código"
                    name="codigo"
                    type="text"
                    value={values.codigo}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.codigo}
                    error={errors.codigo}
                    placeholder="Ej: P-001"
                  />
                </Col>
                <Col md={6}>
                  <CampoFormulario
                    label="Nombre"
                    name="nombre"
                    type="text"
                    value={values.nombre}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.nombre}
                    error={errors.nombre}
                    placeholder="Ej: Milanesa con puré"
                  />
                </Col>
              </Row>

              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Precio"
                    name="precio"
                    type="number"
                    step="0.01"
                    min="0"
                    value={values.precio}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.precio}
                    error={errors.precio}
                    placeholder="Ej: 1500.00"
                  />
                </Col>

                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Sección</Form.Label>
                    <Form.Select
                      name="id_seccion"
                      value={values.id_seccion}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      isInvalid={touched.id_seccion && errors.id_seccion}
                    >
                      <option value="">Seleccione una sección</option>
                      {secciones
                        .filter(s => !s.baja)
                        .map((seccion) => (
                          <option key={seccion.id_seccion} value={seccion.id_seccion}>
                            {seccion.nombre}
                          </option>
                        ))}
                    </Form.Select>
                    {touched.id_seccion && errors.id_seccion && (
                      <Form.Control.Feedback type="invalid">
                        {errors.id_seccion}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col>
                  <CampoFormulario
                    label="Descripción"
                    name="descripcion"
                    as="textarea"
                    rows={3}
                    value={values.descripcion}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.descripcion}
                    error={errors.descripcion}
                    placeholder="Ej: Plato clásico con papas fritas o puré de papas"
                  />
                </Col>
              </Row>
            </Modal.Body>

            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
              </Button>
              <Button variant="primary" type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Guardando...' : editingProducto ? 'Modificar' : 'Crear'}
              </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export default ModalProducto;
