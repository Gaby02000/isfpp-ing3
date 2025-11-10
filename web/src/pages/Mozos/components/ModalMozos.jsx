import React from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik } from 'formik';
import { mozoValidationSchema } from '../../../utils/validations';

const ModalMozo = ({
  show,
  onHide,
  editingMozo,
  onSubmit,
  sectores
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Formik
        initialValues={{
          documento: editingMozo?.documento || '',
          nombre_apellido: editingMozo?.nombre_apellido || '',
          direccion: editingMozo?.direccion || '',
          telefono: editingMozo?.telefono || '',
          id_sector: editingMozo?.id_sector || ''
        }}
        validationSchema={mozoValidationSchema}
        onSubmit={(values, actions) => {
          console.log("Formik onSubmit ejecutado", values); // 👈 Verificación
          onSubmit(values, actions);
        }}
      >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
          <Form onSubmit={handleSubmit}>
            {console.log("Errores actuales:", errors)}
            <Modal.Header closeButton>
              <Modal.Title>
                {editingMozo ? 'Modificar Mozo' : 'Nuevo Mozo'}
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="DNI"
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
                    label="Nombre y Apellido"
                    name="nombre_apellido"
                    type="text"
                    value={values.nombre_apellido}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.nombre_apellido}
                    error={errors.nombre_apellido}
                    placeholder="Ej: Juan Pérez"
                  />
                </Col>
              </Row>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Domicilio"
                    name="direccion"
                    type="text"
                    value={values.direccion}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.direccion}
                    error={errors.direccion}
                    placeholder="Ej: Calle Falsa 123"
                  />
                </Col>
                <Col md={6}>
                  <CampoFormulario
                    label="Teléfono"
                    name="telefono"
                    type="text"
                    value={values.telefono}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.telefono}
                    error={errors.telefono}
                    placeholder="Ej: 2804123456"
                  />
                </Col>
              </Row>
              <Row>
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
                {isSubmitting ? 'Guardando...' : editingMozo ? 'Modificar' : 'Crear'}
              </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export default ModalMozo;