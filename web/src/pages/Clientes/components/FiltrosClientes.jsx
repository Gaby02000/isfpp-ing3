import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosClientes = ({ 
  filtros, 
  onFiltroChange, 
  onLimpiar,
  totalClientes,
  clientesFiltrados
}) => {
  return (
    <div className="mb-4 p-3 bg-light rounded">
      <h5 className="mb-3">🔍 Filtros de Búsqueda</h5>
      <Row className="mb-3"> {/* Fila principal para los filtros de texto */}
        <Col md={4}>
          <Form.Group>
            <Form.Label>Documento</Form.Label>
            <InputGroup>
              <InputGroup.Text>#</InputGroup.Text>
              <Form.Control
                type="text"
                placeholder="Buscar por documento..."
                value={filtros.documento}
                onChange={(e) => onFiltroChange('documento', e.target.value)}
              />
            </InputGroup>
          </Form.Group>
        </Col>

        <Col md={4}>
          <Form.Group>
            <Form.Label>Nombre</Form.Label>
            <InputGroup>
              <InputGroup.Text>👤</InputGroup.Text>
              <Form.Control
                type="text"
                placeholder="Buscar por nombre..."
                value={filtros.nombre}
                onChange={(e) => onFiltroChange('nombre', e.target.value)}
              />
            </InputGroup>
          </Form.Group>
        </Col>

        <Col md={4}>
          <Form.Group>
            <Form.Label>Apellido</Form.Label>
            <InputGroup>
              <InputGroup.Text>👤</InputGroup.Text>
              <Form.Control
                type="text"
                placeholder="Buscar por apellido..."
                value={filtros.apellido}
                onChange={(e) => onFiltroChange('apellido', e.target.value)}
              />
            </InputGroup>
          </Form.Group>
        </Col>
      </Row>
      
      <Row className="mt-2"> {/* Fila para el botón y el contador */}
        <Col>
          <Button variant="outline-secondary" size="sm" onClick={onLimpiar}>
            Limpiar Filtros
          </Button>
          <Badge bg="info" className="ms-2">
            {clientesFiltrados} de {totalClientes} clientes
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosClientes;