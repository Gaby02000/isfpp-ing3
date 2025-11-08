import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosMozos = ({
  filtros,
  onFiltroChange,
  busqueda,
  onBusquedaChange,
  onLimpiar,
  sectores,
  totalMozos,
  mozosFiltrados
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
              placeholder="Buscar por nombre o DNI..."
              value={busqueda}
              onChange={(e) => onBusquedaChange(e.target.value)}
            />
          </InputGroup>
        </Col>
      </Row>

      <Row>
        <Col md={4}>
          <Form.Group>
            <Form.Label>Estado</Form.Label>
            <Form.Select
              value={filtros.activos}
              onChange={(e) => onFiltroChange('activos', e.target.value)}
            >
              <option value="">Todos</option>
              <option value="true">Activos</option>
              <option value="false">Dados de baja</option>
            </Form.Select>
          </Form.Group>
        </Col>

        <Col md={4}>
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
      </Row>

      <Row className="mt-2">
        <Col>
          <Button variant="outline-secondary" size="sm" onClick={onLimpiar}>
            Limpiar Filtros
          </Button>
          <Badge bg="info" className="ms-2">
            {mozosFiltrados} de {totalMozos} mozos
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosMozos;