import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const BarraNavegacion = () => {
  return (
    <Navbar expand="md" bg="light" variant="light">
      <Container>
        <Navbar.Brand as={Link} to="/">UNPSJB</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarNav" />
        <Navbar.Collapse id="navbarNav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Inicio</Nav.Link>
            <Nav.Link as={Link} to="/gestion">Gestión</Nav.Link>
            <NavDropdown title="Mesas" id="nav-dropdown-mesas">
              <NavDropdown.Item as={Link} to="/gestion/mesas">Gestión de Mesas</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Clientes" id="nav-dropdown-clientes">
              <NavDropdown.Item as={Link} to="/gestion/clientes">Gestión de Clientes</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Sectores" id="nav-dropdown-sectores">
              <NavDropdown.Item as={Link} to="/gestion/sectores">Gestión de Sectores</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Mozos" id="nav-dropdown">
              <NavDropdown.Item as={Link} to="/gestion/mozos">Gestión de Mozos</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item as={Link} to="/gestion/mozos/alta">Alta de Mozo</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/gestion/mozos/modificar">Modificar Mozo</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/gestion/mozos/baja">Baja de Mozo</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default BarraNavegacion;