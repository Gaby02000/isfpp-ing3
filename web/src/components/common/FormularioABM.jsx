import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { Formik } from 'formik';
import CampoFormulario from './CampoFormulario';
import MensajeAlerta from './MensajeAlerta';

const FormularioABM = ({
  initialValues,
  validationSchema,
  onSubmit,
  campos,
  submitLabel = 'Guardar',
  submitVariant = 'primary',
  loading = false,
  backPath
}) => {
  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={onSubmit}
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

          {campos.map((campo) => (
            <CampoFormulario
              key={campo.name}
              label={campo.label}
              name={campo.name}
              type={campo.type || 'text'}
              value={values[campo.name]}
              onChange={handleChange}
              onBlur={handleBlur}
              touched={touched[campo.name]}
              error={errors[campo.name]}
              placeholder={campo.placeholder}
              {...campo.props}
            />
          ))}

          <div className="d-flex gap-2 mt-3">
            <Button 
              type="submit" 
              disabled={isSubmitting || loading} 
              variant={submitVariant}
            >
              {isSubmitting || loading ? 'Guardando...' : submitLabel}
            </Button>
            {backPath && (
              <Button 
                variant="outline-secondary"
                onClick={() => window.history.back()}
              >
                Cancelar
              </Button>
            )}
          </div>
        </Form>
      )}
    </Formik>
  );
};

export default FormularioABM;

