import React from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { Formik } from 'formik';
import CampoFormulario from '../../../components/common/CampoFormulario';
import * as Yup from 'yup';

const seccionValidationSchema = Yup.object().shape({
  nombre: Yup.string()
    .required('El nombre es obligatorio')
    .max(255, 'Máximo 255 caracteres'),
});

const ModalSecciones = ({ show, onHide, editingSeccion, onSubmit }) => {
  return (
    <Modal show={show} onHide={onHide} size="md">
      <Formik
        initialValues={{
          nombre: editingSeccion?.nombre || '',
        }}
        validationSchema={seccionValidationSchema}
        onSubmit={(values, actions) => {
          onSubmit(values, actions);
        }}
      >
        {({
          handleSubmit,
          handleChange,
          handleBlur,
          values,
          touched,
          errors,
          isSubmitting,
        }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
              <Modal.Title>
                {editingSeccion ? 'Modificar Sección' : 'Nueva Sección'}
              </Modal.Title>
            </Modal.Header>

            <Modal.Body>
              <CampoFormulario
                label="Nombre de la Sección"
                name="nombre"
                type="text"
                value={values.nombre}
                onChange={handleChange}
                onBlur={handleBlur}
                touched={touched.nombre}
                error={errors.nombre}
                placeholder="Ej: Cocina, Bebidas, Postres..."
              />
            </Modal.Body>

            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
              </Button>
              <Button variant="primary" type="submit" disabled={isSubmitting}>
                {isSubmitting
                  ? 'Guardando...'
                  : editingSeccion
                  ? 'Modificar'
                  : 'Crear'}
              </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export default ModalSecciones;
