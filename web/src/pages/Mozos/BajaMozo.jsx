import React from 'react';
import { Container } from 'react-bootstrap';
import PageHeader from '../../components/common/PageHeader';
import CardAccion from '../../components/common/CardAccion';

const BajaMozo = () => {
  return (
    <Container fluid className="py-4">
      <PageHeader 
        title="Baja de Mozo" 
        backPath="/gestion/mozos" 
      />
      
      <CardAccion
        title="Baja de Mozo"
        variant="info"
        headerVariant="danger"
      />
    </Container>
  );
};

export default BajaMozo;

