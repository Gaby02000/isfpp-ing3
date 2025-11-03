import React from 'react';
import { Container } from 'react-bootstrap';
import PageHeader from '../../components/common/PageHeader';
import CardAccion from '../../components/common/CardAccion';

const ModificarMozo = () => {
  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Modificar Mozo" 
        backPath="/gestion/mozos" 
      />
      
      <CardAccion
        title="Modificar Mozo"
        variant="info"
        headerVariant="warning"
      />
    </Container>
  );
};

export default ModificarMozo;

