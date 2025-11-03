import React from 'react';
import { Card, Button, Container, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const GestionMozos = () => {
  return (
    <Container className="mt-4">
      <h2 className="mb-4">Gestión de Mozos</h2>
      <Row>
        <Col md={4}>
          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Alta de Mozo</Card.Title>
              <Card.Text>Registra un nuevo mozo en el sistema.</Card.Text>
              <Button as={Link} to="/alta-mozo" variant="primary">Ir a Alta</Button>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Baja de Mozo</Card.Title>
              <Card.Text>Da de baja a un mozo del sistema.</Card.Text>
              <Button as={Link} to="/baja-mozo" variant="danger">Ir a Baja</Button>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Modificar Mozo</Card.Title>
              <Card.Text>Actualiza los datos de un mozo existente.</Card.Text>
              <Button as={Link} to="/modificar-mozo" variant="warning">Ir a Modificación</Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default GestionMozos;