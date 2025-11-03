import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NavigationBar = () => {
  return (
    <Navbar expand="md" bg="light" variant="light">
      <Container>
        <Navbar.Brand as={Link} to="/">UNPSJB</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarNav" />
        <Navbar.Collapse id="navbarNav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Inicio</Nav.Link>
            <NavDropdown title="Gestión de Mozos" id="nav-dropdown">
              <NavDropdown.Item as={Link} to="/gestion-mozos">Panel de Gestión</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item as={Link} to="/alta-mozo">Alta de Mozo</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/baja-mozo">Baja de Mozo</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/modificar-mozo">Modificar Mozo</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;