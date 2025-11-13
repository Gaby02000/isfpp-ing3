import React from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik } from 'formik';
import { medioPagoValidationSchema } from '../../../utils/validations';
const ModalMedioPagos = ({ 
  show, 
  onHide,
    editingMedioPago,
    onSubmit
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg"> 
        <Formik
        initialValues={{
          nombre: editingMedioPago?.nombre || '',
          descripcion: editingMedioPago?.descripcion || ''
        }}
        validationSchema={medioPagoValidationSchema}
        onSubmit={onSubmit}
        >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
                <Modal.Title>
                {editingMedioPago ? 'Modificar Medio de Pago' : 'Nuevo Medio de Pago'}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Row>
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
                    placeholder="Ej: Efectivo, Tarjeta..."
                  />
                </Col>
                <Col md={6}>
                  <CampoFormulario
                    label="Descripción"
                    name="descripcion"
                    type="text"
                    value={values.descripcion}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.descripcion}
                    error={errors.descripcion}
                    placeholder="Descripción del medio de pago"
                    />
                </Col>
              </Row>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
                </Button>
                <Button variant="primary" type="submit" disabled={isSubmitting}>
                {editingMedioPago ? 'Guardar Cambios' : 'Crear Medio de Pago'}
                </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
}
export default ModalMedioPagos;