import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

const NavegacionInferior = () => {
  const location = useLocation();

  const navItems = [
    {
      path: '/',
      icon: '🏠',
      label: 'Inicio',
      exact: true
    },
    {
      path: '/gestion',
      icon: '⚙️',
      label: 'Gestión',
      exact: true
    },
    {
      path: '/gestion/mesas',
      icon: '🪑',
      label: 'Mesas'
    },
    {
      path: '/gestion/mozos',
      icon: '👨‍🍳',
      label: 'Mozos'
    },
    {
      path: '/gestion/productos',
      icon: '🍽️',
      label: 'Productos'
    },
    {
      path: '/gestion/medio-pagos',
      icon: '💳',
      label: 'Pagos'
    }
  ];

  const isActive = (item) => {
    if (item.exact) {
      return location.pathname === item.path;
    }
    return location.pathname.startsWith(item.path);
  };

  return (
    <Navbar 
      fixed="bottom" 
      bg="light" 
      variant="light" 
      className="border-top shadow-sm"
      style={{ 
        height: '60px',
        paddingTop: '0',
        paddingBottom: '0'
      }}
    >
      <Nav className="w-100 d-flex justify-content-around align-items-center" style={{ height: '100%' }}>
        {navItems.map((item) => {
          const active = isActive(item);
          return (
            <Nav.Link
              key={item.path}
              as={Link}
              to={item.path}
              className={`d-flex flex-column align-items-center justify-content-center ${
                active ? 'text-primary' : 'text-muted'
              }`}
              style={{
                minWidth: '60px',
                height: '100%',
                padding: '4px 8px',
                textDecoration: 'none',
                transition: 'all 0.2s',
                borderTop: active ? '3px solid #0d6efd' : '3px solid transparent'
              }}
            >
              <span style={{ fontSize: '1.5rem', lineHeight: '1' }}>{item.icon}</span>
              <small style={{ fontSize: '0.7rem', marginTop: '2px', fontWeight: active ? '600' : '400' }}>
                {item.label}
              </small>
            </Nav.Link>
          );
        })}
      </Nav>
    </Navbar>
  );
};

export default NavegacionInferior;

