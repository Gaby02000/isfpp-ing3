import React from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { Formik } from 'formik';
import { sectorValidationSchema } from '../../../utils/validations';
import CampoFormulario from '../../../components/common/CampoFormulario';

const ModalSector = ({ 
  show, 
  onHide, 
  editingSector, 
  onSubmit 
}) => {
  return (
    <Modal show={show} onHide={onHide}>
      <Formik
        initialValues={{
          numero: editingSector?.numero || ''
        }}
        validationSchema={sectorValidationSchema}
        onSubmit={onSubmit}
      >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
              <Modal.Title>
                {editingSector ? 'Modificar Sector' : 'Nuevo Sector'}
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <CampoFormulario
                label="Número de Sector"
                name="numero"
                type="number"
                value={values.numero}
                onChange={handleChange}
                onBlur={handleBlur}
                touched={touched.numero}
                error={errors.numero}
                placeholder="Ej: 1, 2, 3..."
              />
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
              </Button>
              <Button variant="primary" type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Guardando...' : editingSector ? 'Modificar' : 'Crear'}
              </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export default ModalSector;

