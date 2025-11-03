import React from 'react';
import { Form } from 'react-bootstrap';

const CampoFormulario = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  onBlur,
  touched,
  error,
  placeholder,
  ...props
}) => {
  return (
    <Form.Group className="mb-3">
      <Form.Label>{label}</Form.Label>
      <Form.Control
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        placeholder={placeholder}
        isInvalid={touched && error}
        {...props}
      />
      {touched && error && (
        <Form.Control.Feedback type="invalid">
          {error}
        </Form.Control.Feedback>
      )}
    </Form.Group>
  );
};

export default CampoFormulario;

