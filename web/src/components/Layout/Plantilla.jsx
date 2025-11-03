import React from 'react';
import { Container } from 'react-bootstrap';
import BarraNavegacion from './BarraNavegacion';

const Plantilla = ({ children }) => {
  return (
    <>
      <BarraNavegacion />
      <Container>
        {children}
      </Container>
    </>
  );
};

export default Plantilla;