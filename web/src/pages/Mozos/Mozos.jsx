import React from 'react';
import { Card, Row, Col, Button, Container } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';

const Mozos = () => {
  const navigate = useNavigate();

  const accionesMozos = [
    {
      title: 'Alta de Mozo',
      description: 'Registra un nuevo mozo en el sistema',
      icon: '➕',
      path: '/gestion/mozos/alta',
      variant: 'success'
    },
    {
      title: 'Modificar Mozo',
      description: 'Actualiza los datos de un mozo existente',
      icon: '✏️',
      path: '/gestion/mozos/modificar',
      variant: 'warning'
    },
    {
      title: 'Baja de Mozo',
      description: 'Da de baja a un mozo del sistema',
      icon: '🗑️',
      path: '/gestion/mozos/baja',
      variant: 'danger'
    }
  ];

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <div className="d-flex align-items-center mb-3">
            <Button 
              variant="outline-secondary" 
              onClick={() => navigate('/gestion')}
              className="me-3"
            >
              ← Volver
            </Button>
            <div>
              <h1 className="display-5 mb-2">Gestión de Mozos</h1>
              <p className="lead text-muted">
                Administra todos los mozos del sistema
              </p>
            </div>
          </div>
        </Col>
      </Row>

      <Row>
        {accionesMozos.map((accion, index) => (
          <Col md={6} lg={4} key={index} className="mb-4">
            <Card 
              className="shadow-sm border-0 h-100"
              style={{ transition: 'transform 0.2s', cursor: 'pointer' }}
              onClick={() => navigate(accion.path)}
            >
              <Card.Body className="d-flex flex-column text-center">
                <div className="mb-3">
                  <div style={{ fontSize: '4rem' }}>{accion.icon}</div>
                </div>
                <Card.Title className="mb-3">{accion.title}</Card.Title>
                <Card.Text className="text-muted flex-grow-1 mb-4">
                  {accion.description}
                </Card.Text>
                <Button 
                  variant={accion.variant} 
                  as={Link} 
                  to={accion.path}
                  className="w-100"
                >
                  Acceder
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default Mozos;

