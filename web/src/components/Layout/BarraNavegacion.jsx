import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const BarraNavegacion = () => {
  return (
    <Navbar bg="primary" variant="dark" className="shadow-sm">
      <Container>
        <Navbar.Brand 
          as={Link} 
          to="/" 
          className="fw-bold"
          style={{ fontSize: '1.5rem' }}
        >
          🍽️ UNPSJB - Sistema de Gestión
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default BarraNavegacion;