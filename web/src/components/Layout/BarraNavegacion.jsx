import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
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
    '/gestion/medio-pagos': 'Medios de Pago',
    '/gestion/clientes': 'Gestión de Clientes'
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