import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosSectores = ({ 
  filtros, 
  onFiltroChange, 
  busqueda,
  onBusquedaChange,
  onLimpiar,
  totalSectores,
  sectoresFiltrados
}) => {
  return (
    <div className="mb-4 p-3 bg-light rounded">
      <h5 className="mb-3">🔍 Filtros de Búsqueda</h5>
      <Row className="mb-3">
        <Col md={6}>
          <InputGroup>
            <InputGroup.Text>🔎</InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Buscar por número..."
              value={busqueda}
              onChange={(e) => onBusquedaChange(e.target.value)}
            />
          </InputGroup>
        </Col>
      </Row>
      <Row>
        <Col md={4}>
          <Form.Group>
            <Form.Label>Número de Sector</Form.Label>
            <Form.Control
              type="number"
              placeholder="Ej: 1, 2, 3..."
              value={filtros.numero}
              onChange={(e) => onFiltroChange('numero', e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={4}>
          <Form.Group>
            <Form.Label>Estado</Form.Label>
            <Form.Select
              value={filtros.estado}
              onChange={(e) => onFiltroChange('estado', e.target.value)}
            >
              <option value="">Todos</option>
              <option value="activo">Activos</option>
              <option value="baja">Dados de baja</option>
            </Form.Select>
          </Form.Group>
        </Col>
        <Col md={4} className="d-flex align-items-end">
          <Button variant="outline-secondary" size="sm" onClick={onLimpiar}>
            Limpiar Filtros
          </Button>
          <Badge bg="info" className="ms-2">
            {sectoresFiltrados} de {totalSectores} sectores
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosSectores;

