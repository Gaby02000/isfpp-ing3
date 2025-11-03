import React from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import { Formik } from 'formik';
import * as Yup from 'yup';
import { useMozoService } from '../../services/mozoService';
import { mozoValidationSchema } from '../../utils/validations';
import MensajeAlerta from '../../components/common/MensajeAlerta';
import CampoFormulario from '../../components/common/CampoFormulario';
import PageHeader from '../../components/common/PageHeader';

const AltaMozo = () => {
  const { createMozo } = useMozoService();

  const handleSubmit = async (values, { setSubmitting, setStatus, resetForm }) => {
    try {
      await createMozo(values);
      setStatus({ success: 'Mozo creado exitosamente' });
      resetForm();
    } catch (error) {
      setStatus({ error: error.message || 'Error al crear el mozo' });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Alta de Mozo" 
        backPath="/gestion/mozos" 
      />
      
      <Formik
        initialValues={{
          dni: '',
          nombre: '',
          apellido: '',
          domicilio: '',
          telefono: '',
          sector: ''
        }}
        validationSchema={mozoValidationSchema}
        onSubmit={handleSubmit}
      >
        {({
          handleSubmit,
          handleChange,
          handleBlur,
          values,
          touched,
          errors,
          isSubmitting,
          status
        }) => (
          <Form onSubmit={handleSubmit}>
            {status?.success && (
              <MensajeAlerta variant="success" message={status.success} />
            )}
            
            {status?.error && (
              <MensajeAlerta variant="danger" message={status.error} />
            )}

            <CampoFormulario
              label="DNI"
              name="dni"
              type="text"
              value={values.dni}
              onChange={handleChange}
              onBlur={handleBlur}
              touched={touched.dni}
              error={errors.dni}
            />

            <CampoFormulario
              label="Nombre"
              name="nombre"
              type="text"
              value={values.nombre}
              onChange={handleChange}
              onBlur={handleBlur}
              touched={touched.nombre}
              error={errors.nombre}
            />

            <CampoFormulario
              label="Apellido"
              name="apellido"
              type="text"
              value={values.apellido}
              onChange={handleChange}
              onBlur={handleBlur}
              touched={touched.apellido}
              error={errors.apellido}
            />

            <CampoFormulario
              label="Domicilio"
              name="domicilio"
              type="text"
              value={values.domicilio}
              onChange={handleChange}
              onBlur={handleBlur}
              touched={touched.domicilio}
              error={errors.domicilio}
            />

            <CampoFormulario
              label="Teléfono"
              name="telefono"
              type="text"
              value={values.telefono}
              onChange={handleChange}
              onBlur={handleBlur}
              touched={touched.telefono}
              error={errors.telefono}
            />

            <CampoFormulario
              label="Sector"
              name="sector"
              type="text"
              value={values.sector}
              onChange={handleChange}
              onBlur={handleBlur}
              touched={touched.sector}
              error={errors.sector}
            />

            <Button type="submit" disabled={isSubmitting} variant="primary">
              {isSubmitting ? 'Creando...' : 'Crear Mozo'}
            </Button>
          </Form>
        )}
      </Formik>
    </Container>
  );
};

export default AltaMozo;

