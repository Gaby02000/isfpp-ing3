import React from 'react';
import { Spinner } from 'react-bootstrap';

const Cargador = ({ size = 'md', className = '', variant = 'primary' }) => {
  return (
    <Spinner 
      animation="border" 
      role="status" 
      size={size}
      variant={variant}
      className={className}
    >
      <span className="visually-hidden">Cargando...</span>
    </Spinner>
  );
};

export default Cargador;

