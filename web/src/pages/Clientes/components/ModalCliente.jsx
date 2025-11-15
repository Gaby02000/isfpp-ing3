import React from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik } from 'formik';
// 1. IMPORTANTE: Debes crear e importar un esquema de validación para Cliente
import { clienteValidationSchema } from '../../../utils/validations'; 

const ModalCliente = ({ 
  show, 
  onHide, 
  editingCliente, // 2. Renombramos la prop
  onSubmit 
  // 3. Quitamos 'sectores' y 'tiposMesas' (ya no se necesitan)
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Formik
        // 4. Actualizamos los valores iniciales
        initialValues={{
          documento: editingCliente?.documento || '',
          nombre: editingCliente?.nombre || '',
          apellido: editingCliente?.apellido || '',
          num_telefono: editingCliente?.num_telefono || '',
          email: editingCliente?.email || ''
        }}
        // 5. Usamos el nuevo esquema de validación
        validationSchema={clienteValidationSchema} 
        onSubmit={onSubmit}
      >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
              <Modal.Title>
                {/* 6. Actualizamos el título */}
                {editingCliente ? 'Modificar Cliente' : 'Nuevo Cliente'}
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              {/* 7. Reemplazamos todos los campos */}
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Documento"
                    name="documento"
                    type="text"
                    value={values.documento}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.documento}
                    error={errors.documento}
                    placeholder="Ej: 12345678"
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
                    placeholder="Ej: Juan"
                  />
                </Col>
              </Row>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Apellido"
                    name="apellido"
                    type="text"
                    value={values.apellido}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.apellido}
                    error={errors.apellido}
                    placeholder="Ej: Pérez"
                  />
                </Col>
                <Col md={6}>
                  <CampoFormulario
                    label="Número de Teléfono"
                    name="num_telefono"
                    type="text"
                    value={values.num_telefono}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.num_telefono}
                    error={errors.num_telefono}
                    placeholder="Ej: 2804123456"
                  />
                </Col>
              </Row>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Email"
                    name="email"
                    type="email"
                    value={values.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.email}
                    error={errors.email}
                    placeholder="Ej: juan.perez@correo.com"
                  />
                </Col>
              </Row>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
              </Button>
              <Button variant="primary" type="submit" disabled={isSubmitting}>
                {/* 8. Actualizamos el texto del botón */}
                {isSubmitting ? 'Guardando...' : editingCliente ? 'Modificar' : 'Crear'}
              </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export default ModalCliente;