import React from 'react';
import { Container, Form, Button, Alert } from 'react-bootstrap';
import { Formik } from 'formik';
import * as Yup from 'yup';
import { useMozoService } from '../../services/mozoService';

const validationSchema = Yup.object({
  dni: Yup.string()
    .required('El DNI es requerido')
    .matches(/^\d+$/, 'El DNI debe contener solo números'),
  nombre: Yup.string()
    .required('El nombre es requerido'),
  apellido: Yup.string()
    .required('El apellido es requerido'),
  domicilio: Yup.string()
    .required('El domicilio es requerido'),
  telefono: Yup.string()
    .required('El teléfono es requerido')
    .matches(/^\d+$/, 'El teléfono debe contener solo números'),
  sector: Yup.string()
    .required('El sector es requerido')
});

const AltaMozo = () => {
  const { createMozo } = useMozoService();

  const handleSubmit = async (values, { setSubmitting, setStatus }) => {
    try {
      await createMozo(values);
      setStatus({ success: 'Mozo creado exitosamente' });
    } catch (error) {
      setStatus({ error: error.message || 'Error al crear el mozo' });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Alta de Mozo</h2>
      
      <Formik
        initialValues={{
          dni: '',
          nombre: '',
          apellido: '',
          domicilio: '',
          telefono: '',
          sector: ''
        }}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({
          handleSubmit,
          handleChange,
          values,
          touched,
          errors,
          isSubmitting,
          status
        }) => (
          <Form onSubmit={handleSubmit}>
            {status?.success && (
              <Alert variant="success">{status.success}</Alert>
            )}
            
            {status?.error && (
              <Alert variant="danger">{status.error}</Alert>
            )}

            <Form.Group className="mb-3">
              <Form.Label>DNI</Form.Label>
              <Form.Control
                type="text"
                name="dni"
                value={values.dni}
                onChange={handleChange}
                isInvalid={touched.dni && errors.dni}
              />
              <Form.Control.Feedback type="invalid">
                {errors.dni}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Nombre</Form.Label>
              <Form.Control
                type="text"
                name="nombre"
                value={values.nombre}
                onChange={handleChange}
                isInvalid={touched.nombre && errors.nombre}
              />
              <Form.Control.Feedback type="invalid">
                {errors.nombre}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Apellido</Form.Label>
              <Form.Control
                type="text"
                name="apellido"
                value={values.apellido}
                onChange={handleChange}
                isInvalid={touched.apellido && errors.apellido}
              />
              <Form.Control.Feedback type="invalid">
                {errors.apellido}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Domicilio</Form.Label>
              <Form.Control
                type="text"
                name="domicilio"
                value={values.domicilio}
                onChange={handleChange}
                isInvalid={touched.domicilio && errors.domicilio}
              />
              <Form.Control.Feedback type="invalid">
                {errors.domicilio}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Teléfono</Form.Label>
              <Form.Control
                type="text"
                name="telefono"
                value={values.telefono}
                onChange={handleChange}
                isInvalid={touched.telefono && errors.telefono}
              />
              <Form.Control.Feedback type="invalid">
                {errors.telefono}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Sector</Form.Label>
              <Form.Control
                type="text"
                name="sector"
                value={values.sector}
                onChange={handleChange}
                isInvalid={touched.sector && errors.sector}
              />
              <Form.Control.Feedback type="invalid">
                {errors.sector}
              </Form.Control.Feedback>
            </Form.Group>

            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Creando...' : 'Crear Mozo'}
            </Button>
          </Form>
        )}
      </Formik>
    </Container>
  );
};

export default AltaMozo;