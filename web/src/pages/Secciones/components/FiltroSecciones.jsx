import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltroSecciones = ({
  filtros,
  onFiltroChange,
  busqueda,
  onBusquedaChange,
  onLimpiar,
  totalSecciones,
  seccionesFiltradas
}) => {
  return (
    <div className="mb-4 p-3 bg-light rounded">
      <h5 className="mb-3">📂 Filtros de Secciones</h5>

      <Row className="mb-3">
        <Col md={6}>
          <InputGroup>
            <InputGroup.Text>🔎</InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Buscar por nombre de sección..."
              value={busqueda}
              onChange={(e) => onBusquedaChange(e.target.value)}
            />
          </InputGroup>
        </Col>
      </Row>

      <Row>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Estado</Form.Label>
            <Form.Select
              value={filtros.activos}
              onChange={(e) => onFiltroChange('activos', e.target.value)}
            >
              <option value="">Todas</option>
              <option value="true">Activas</option>
              <option value="false">Dadas de baja</option>
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>

      <Row className="mt-3">
        <Col>
          <Button variant="outline-secondary" size="sm" onClick={onLimpiar}>
            Limpiar Filtros
          </Button>
          <Badge bg="info" className="ms-2">
            {seccionesFiltradas} de {totalSecciones} secciones
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltroSecciones;
