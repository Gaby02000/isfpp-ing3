import React from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik } from 'formik';
import { mesaValidationSchema } from '../../../utils/validations';

const ModalMesa = ({ 
  show, 
  onHide, 
  editingMesa, 
  onSubmit, 
  sectores,
  tiposMesas
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Formik
        initialValues={{
          numero: editingMesa?.numero || '',
          tipo: editingMesa?.tipo || '',
          cant_comensales: editingMesa?.cant_comensales || '',
          id_sector: editingMesa?.id_sector || ''
        }}
        validationSchema={mesaValidationSchema}
        onSubmit={onSubmit}
      >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
              <Modal.Title>
                {editingMesa ? 'Modificar Mesa' : 'Nueva Mesa'}
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Número de Mesa"
                    name="numero"
                    type="number"
                    value={values.numero}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.numero}
                    error={errors.numero}
                    placeholder="Ej: 1, 2, 3..."
                  />
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Tipo</Form.Label>
                    <Form.Select
                      name="tipo"
                      value={values.tipo}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      isInvalid={touched.tipo && errors.tipo}
                    >
                      <option value="">Seleccione un tipo</option>
                      {tiposMesas.map((tipo) => (
                        <option key={tipo} value={tipo}>
                          {tipo}
                        </option>
                      ))}
                    </Form.Select>
                    {touched.tipo && errors.tipo && (
                      <Form.Control.Feedback type="invalid">
                        {errors.tipo}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>
                </Col>
              </Row>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Cantidad de Comensales"
                    name="cant_comensales"
                    type="number"
                    value={values.cant_comensales}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.cant_comensales}
                    error={errors.cant_comensales}
                    placeholder="Ej: 4, 6, 8..."
                  />
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Sector</Form.Label>
                    <Form.Select
                      name="id_sector"
                      value={values.id_sector}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      isInvalid={touched.id_sector && errors.id_sector}
                    >
                      <option value="">Seleccione un sector</option>
                      {sectores
                        .filter(s => !s.baja)
                        .map((sector) => (
                          <option key={sector.id_sector} value={sector.id_sector}>
                            Sector {sector.numero} ({sector.cantidad_mesas || 0} mesas)
                          </option>
                        ))}
                    </Form.Select>
                    {touched.id_sector && errors.id_sector && (
                      <Form.Control.Feedback type="invalid">
                        {errors.id_sector}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>
                </Col>
              </Row>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
              </Button>
              <Button variant="primary" type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Guardando...' : editingMesa ? 'Modificar' : 'Crear'}
              </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export default ModalMesa;

