import React from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import CampoFormulario from '../../../components/common/CampoFormulario';
import { Formik } from 'formik';
import { reservaValidationSchema } from '../../../utils/validations'; // debes definir este schema

const ModalReservas = ({
  show,
  onHide,
  editingReserva,
  onSubmit,
  clientes,
  mesas,
  // Si true enviamos ISO UTC, si false enviamos 'YYYY-MM-DD HH:MM:SS' (preserva hora local)
  sendUtc = false
}) => {

  // Helpers para convertir formatos de fecha entre backend, input datetime-local y envio
  const pad = (n) => String(n).padStart(2, '0');

  // Convierte string backend o ISO a formato aceptado por input datetime-local: 'YYYY-MM-DDTHH:MM'
  const formatDateToDateTimeLocal = (input) => {
    if (!input) return '';
    let s = String(input).trim();
    // Reemplazar espacio por T si viene como 'YYYY-MM-DD HH:MM:SS'
    if (s.includes(' ') && !s.includes('T')) s = s.replace(' ', 'T');
    // Añadir segundos si falta
    if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(s)) s = s + ':00';

    const d = new Date(s);
    if (isNaN(d.getTime())) return '';
    const year = d.getFullYear();
    const month = pad(d.getMonth() + 1);
    const day = pad(d.getDate());
    const hour = pad(d.getHours());
    const minute = pad(d.getMinutes());
    return `${year}-${month}-${day}T${hour}:${minute}`;
  };

  // Convierte 'YYYY-MM-DDTHH:MM' a 'YYYY-MM-DD HH:MM:SS' (preserva hora local)
  const dateTimeLocalToBackendFormat = (localString) => {
    if (!localString) return null;
    const t = localString.replace('T', ' ');
    if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(t)) return t + ':00';
    return t;
  };

  // Convierte 'YYYY-MM-DDTHH:MM' a ISO UTC (toISOString)
  const dateTimeLocalToISOStringUTC = (localString) => {
    if (!localString) return null;
    // Crear Date usando la interpretación local
    const d = new Date(localString);
    if (isNaN(d.getTime())) return null;
    return d.toISOString();
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Formik
        initialValues={{
          numero: editingReserva?.numero || '',
          fecha_hora: editingReserva ? formatDateToDateTimeLocal(editingReserva.fecha_hora) : '',
          cant_personas: editingReserva?.cant_personas || '',
          id_cliente: editingReserva?.id_cliente || '',
          id_mesa: editingReserva?.id_mesa || '',
        }}
        validationSchema={reservaValidationSchema}
        onSubmit={(values, actions) => {
          // Convertir fecha antes de enviar al parent
          const out = { ...values };
          if (values.fecha_hora) {
            if (sendUtc) {
              out.fecha_hora = dateTimeLocalToISOStringUTC(values.fecha_hora);
            } else {
              out.fecha_hora = dateTimeLocalToBackendFormat(values.fecha_hora);
            }
          }
          onSubmit(out, actions);
        }}
      >
        {({ handleSubmit, handleChange, handleBlur, values, touched, errors, isSubmitting }) => (
          <Form onSubmit={handleSubmit}>
            <Modal.Header closeButton>
              <Modal.Title>
                {editingReserva ? 'Modificar Reserva' : 'Nueva Reserva'}
              </Modal.Title>
            </Modal.Header>

            <Modal.Body>
              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Número de Reserva"
                    name="numero"
                    type="text"
                    value={values.numero}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.numero}
                    error={errors.numero}
                    placeholder="Ej: 1001"
                  />
                </Col>
                <Col md={6}>
                  <CampoFormulario
                    label="Fecha y Hora"
                    name="fecha_hora"
                    type="datetime-local"
                    value={values.fecha_hora}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.fecha_hora}
                    error={errors.fecha_hora}
                  />
                </Col>
              </Row>

              <Row>
                <Col md={6}>
                  <CampoFormulario
                    label="Cantidad de Personas"
                    name="cant_personas"
                    type="number"
                    min="1"
                    value={values.cant_personas}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    touched={touched.cant_personas}
                    error={errors.cant_personas}
                    placeholder="Ej: 4"
                  />
                </Col>

                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Cliente</Form.Label>
                    <Form.Select
                      name="id_cliente"
                      value={values.id_cliente || ''}   
                      onChange={handleChange}
                      onBlur={handleBlur}
                      isInvalid={touched.id_cliente && errors.id_cliente}
                    >
                      <option value="">Seleccione un cliente</option>
                      {clientes
                        .filter(c => !c.baja)
                        .map((cliente) => (
                          <option key={cliente.id_cliente} value={cliente.id_cliente}>
                            {cliente.nombre} {cliente.apellido}   {/* 👈 corregido */}
                          </option>
                        ))}
                    </Form.Select>
                    {touched.id_cliente && errors.id_cliente && (
                      <Form.Control.Feedback type="invalid">
                        {errors.id_cliente}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Mesa</Form.Label>
                    <Form.Select
                      name="id_mesa"
                      value={values.id_mesa || ''} 
                      onChange={handleChange}
                      onBlur={handleBlur}
                      isInvalid={touched.id_mesa && errors.id_mesa}
                    >
                      <option value="">Seleccione una mesa</option>
                      {mesas
                        .filter(m => !m.baja)
                        .map((mesa) => (
                          <option key={mesa.id_mesa} value={mesa.id_mesa}>
                            Mesa {mesa.numero} ({mesa.tipo}, {mesa.cant_comensales} personas)
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
              </Row>
            </Modal.Body>

            <Modal.Footer>
              <Button variant="secondary" onClick={onHide}>
                Cancelar
              </Button>
              <Button variant="primary" type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Guardando...' : editingReserva ? 'Modificar' : 'Crear'}
              </Button>
            </Modal.Footer>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export default ModalReservas;