import React from 'react';
import { Container } from 'react-bootstrap';
import BarraNavegacion from './BarraNavegacion';
import NavegacionInferior from './NavegacionInferior';

const Plantilla = ({ children }) => {
  return (
    <>
      <BarraNavegacion />
      <Container className="pb-5 mb-5" style={{ paddingBottom: '80px' }}>
        {children}
      </Container>
      <NavegacionInferior />
    </>
  );
};

export default Plantilla;