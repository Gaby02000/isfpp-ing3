import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosMesas = ({ 
  filtros, 
  onFiltroChange, 
  busqueda,
  onBusquedaChange,
  onLimpiar,
  sectores,
  totalMesas,
  mesasFiltradas
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
              placeholder="Buscar por número o tipo..."
              value={busqueda}
              onChange={(e) => onBusquedaChange(e.target.value)}
            />
          </InputGroup>
        </Col>
      </Row>
      <Row>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Número de Mesa</Form.Label>
            <Form.Control
              type="number"
              placeholder="Ej: 1, 2, 3..."
              value={filtros.numero}
              onChange={(e) => onFiltroChange('numero', e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Sector</Form.Label>
            <Form.Select
              value={filtros.sector_id}
              onChange={(e) => onFiltroChange('sector_id', e.target.value)}
            >
              <option value="">Todos los sectores</option>
              {sectores
                .filter(s => !s.baja)
                .map((sector) => (
                  <option key={sector.id_sector} value={sector.id_sector}>
                    Sector {sector.numero}
                  </option>
                ))}
            </Form.Select>
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Tipo</Form.Label>
            <Form.Select
              value={filtros.tipo}
              onChange={(e) => onFiltroChange('tipo', e.target.value)}
            >
              <option value="">Todos los tipos</option>
              <option value="interior">Interior</option>
              <option value="exterior">Exterior</option>
              <option value="vip">VIP</option>
            </Form.Select>
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Estado</Form.Label>
            <Form.Select
              value={filtros.estado}
              onChange={(e) => onFiltroChange('estado', e.target.value)}
            >
              <option value="">Todos</option>
              <option value="activa">Activas</option>
              <option value="baja">Dadas de baja</option>
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>
      <Row className="mt-2">
        <Col>
          <Button variant="outline-secondary" size="sm" onClick={onLimpiar}>
            Limpiar Filtros
          </Button>
          <Badge bg="info" className="ms-2">
            {mesasFiltradas} de {totalMesas} mesas
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosMesas;

