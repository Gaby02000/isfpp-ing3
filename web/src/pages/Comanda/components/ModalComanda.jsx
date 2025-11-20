import React from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik } from 'formik';
import { comandaValidationSchema } from '../../../utils/validations';

const ModalComanda = ({ 
  show, 
  onHide,
    editingComanda,
    onSubmit,
    mesas,
    mozos,
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg">
        <Formik
        initialValues={{
            fecha : editingComanda?.fecha || '',
            id_mesa: editingComanda?.id_mesa || '',
            id_mozo: editingComanda?.id_mozo || ''
        }}
        validationSchema={comandaValidationSchema}
        onSubmit={onSubmit}
        >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
            <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
                <Modal.Title>
                {editingComanda ? 'Modificar Comanda' : 'Nueva Comanda'}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Row>
                <Col md={6}>
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
                <Col md={6}>
                    <Form.Group className="mb-3">
                    <Form.Label>Mesa</Form.Label>
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
                            Mesa {mesa.numero}
                            </option>   
                        ))}
                    </Form.Select>
                    {touched.id_mesa && errors.id_mesa && (
                        <Form.Control.Feedback type="invalid">
                        {errors.id_mesa}
                        </Form.Control.Feedback>
                    )}
                    </Form.Group>
                </Col>
                <Col md={6}>
                    <Form.Group className="mb-3">
                    <Form.Label>Mozo</Form.Label>
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
                            <option key={mozo.id_mozo} value={mozo.id_mozo}>
                            {mozo.nombre}
                            </option>
                        ))}
                    </Form.Select>
                    {touched.id_mozo && errors.id_mozo && (
                        <Form.Control.Feedback type="invalid">
                        {errors.id_mozo}
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
                {editingComanda ? 'Guardar Cambios' : 'Crear Comanda'}
                </Button>
            </Modal.Footer>
            </Form>
        )}  
        </Formik>
    </Modal>
  );
}

export default ModalComanda;