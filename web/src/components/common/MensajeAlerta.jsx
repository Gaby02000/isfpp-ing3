import React from 'react';
import { Alert } from 'react-bootstrap';

const MensajeAlerta = ({ 
  variant = 'info', 
  message, 
  heading, 
  dismissible = false,
  onClose,
  className = ''
}) => {
  if (!message) return null;

  return (
    <Alert 
      variant={variant} 
      dismissible={dismissible}
      onClose={onClose}
      className={className}
    >
      {heading && <Alert.Heading>{heading}</Alert.Heading>}
      {message}
    </Alert>
  );
};

export default MensajeAlerta;

