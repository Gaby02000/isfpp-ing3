import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import MensajeAlerta from './MensajeAlerta';

const CardAccion = ({ 
  title, 
  variant = 'info',
  headerVariant = 'warning',
  message = 'Esta funcionalidad está siendo desarrollada y estará disponible próximamente.',
  backPath = '/gestion/mozos',
  backLabel = 'Volver a Gestión de Mozos'
}) => {
  const navigate = useNavigate();
  
  return (
    <Card className="shadow-sm">
      <Card.Header as="h4" className={`bg-${headerVariant} ${headerVariant === 'warning' ? 'text-dark' : 'text-white'}`}>
        {title}
      </Card.Header>
      <Card.Body>
        <MensajeAlerta
          variant={variant}
          heading="Funcionalidad en desarrollo"
          message={message}
        />
        <Button 
          variant="secondary" 
          className="mt-3"
          onClick={() => navigate(backPath)}
        >
          {backLabel}
        </Button>
      </Card.Body>
    </Card>
  );
};

export default CardAccion;

