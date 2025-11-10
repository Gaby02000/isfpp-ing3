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
            <NavDropdown title="Productos" id="nav-dropdown-productos">
              <NavDropdown.Item as={Link} to="/gestion/productos">Gestión de Productos</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item as={Link} to="/gestion/productos/alta">Alta de Producto</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/gestion/productos/modificar">Modificar Producto</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/gestion/productos/baja">Baja de Producto</NavDropdown.Item>
            </NavDropdown>
                <NavDropdown title="Secciones" id="nav-dropdown-secciones">
              <NavDropdown.Item as={Link} to="/gestion/secciones">Gestión de Secciones</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item as={Link} to="/gestion/secciones/alta">Alta de Sección</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/gestion/secciones/modificar">Modificar Sección</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/gestion/secciones/baja">Baja de Sección</NavDropdown.Item>
            </NavDropdown>

          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default BarraNavegacion;