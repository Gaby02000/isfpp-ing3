import React from 'react';
import { Card, Row, Col, Button, Container } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';

const Gestion = () => {
  const navigate = useNavigate();

  const areasGestion = [
    {
      title: 'Mesas',
      description: 'Administra todas las mesas del restaurante: Alta, Baja y Modificación',
      icon: '🪑',
      path: '/gestion/mesas',
      variant: 'primary'
    },
    {
      title: 'Sectores',
      description: 'Administra los sectores del salón: Alta, Baja y Modificación',
      icon: '🏠️',
      path: '/gestion/sectores',
      variant: 'info'
    },
    {
      title: 'Mozos',
      description: 'Administra todos los mozos del sistema: Alta, Baja y Modificación',
      icon: '👨‍🍳',
      path: '/gestion/mozos',
      variant: 'success'
    },
    {
      title: 'Productos',
      description: 'Administra productos, platos, postres y bebidas del menú',
      icon: '🍽️',
      path: '/gestion/productos',
      variant: 'success',
      disabled: true
    },
    {
      title: 'Clientes',
      descripcion: 'Administra los clientes del sistema: Alta, Baja y Modificación',
      icon: '👥',
      path: 'gestion/clientes',
      variant: 'success'


    },
    {
      title: 'Secciones',
      description: 'Gestiona las secciones del menú y su organización',
      icon: '📋',
      path: '/gestion/secciones',
      variant: 'secondary'
    },
    {
      title: 'Medios de Pago',
      description: 'Administra los medios de pago disponibles en el sistema',
      icon: '💳',
      path: '/gestion/medio-pagos',
      variant: 'light'
    }
  ];

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <h1 className="display-4 mb-2">Panel de Gestión</h1>
          <p className="lead text-muted">
            Selecciona el área que deseas gestionar
          </p>
        </Col>
      </Row>

      <Row>
        {areasGestion.map((area, index) => (
          <Col md={6} lg={4} key={index} className="mb-4">
            <Card
              className={`shadow-sm border-0 h-100 ${area.disabled ? 'opacity-50' : ''}`}
              style={{
                transition: 'transform 0.2s',
                cursor: area.disabled ? 'not-allowed' : 'pointer'
              }}
              onClick={() => !area.disabled && navigate(area.path)}
            >
              <Card.Body className="d-flex flex-column text-center">
                <div className="mb-3">
                  <div style={{ fontSize: '4rem' }}>{area.icon}</div>
                </div>
                <Card.Title className="mb-3">{area.title}</Card.Title>
                <Card.Text className="text-muted flex-grow-1 mb-4">
                  {area.description}
                </Card.Text>
                <Button
                  variant={area.variant}
                  as={Link}
                  to={area.path}
                  className="w-100"
                  disabled={area.disabled}
                >
                  {area.disabled ? 'Próximamente' : 'Acceder'}
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default Gestion;
