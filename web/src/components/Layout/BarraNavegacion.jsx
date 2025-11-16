import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

const BarraNavegacion = () => {
  const location = useLocation();

  const pageTitles = {
    '/': 'Panel de Administración',
    '/gestion': 'Panel de Gestión',
    '/gestion/mesas': 'Gestión de Mesas',
    '/gestion/mozos': 'Gestión de Mozos',
    '/gestion/sectores': 'Gestión de Sectores',
    '/gestion/productos': 'Gestión de Productos',
    '/gestion/secciones': 'Gestión de Secciones',
    '/gestion/medio-pagos': 'Medios de Pago'
  };

  const getPageTitle = () => {
    for (const [path, title] of Object.entries(pageTitles)) {
      if (location.pathname === path) {
        return title;
      }
      if (path !== '/' && location.pathname.startsWith(path)) {
        return title;
      }
    }
    return 'Sistema de Gestión';
  };

  const currentTitle = getPageTitle();

  return (
    <Navbar bg="primary" variant="dark" className="shadow-sm">
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
        <Navbar.Brand 
          as={Link} 
          to="/" 
          className="fw-bold d-flex align-items-center"
          style={{ fontSize: '1.5rem' }}
        >
          <span className="me-2">🍽️</span>
          <span>{currentTitle}</span>
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default BarraNavegacion;