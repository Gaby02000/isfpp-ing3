import React, { useState, useEffect } from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosPagos = ({ 
  filtros, 
  onFiltroChange,
  busqueda,
  onBusquedaChange,
  onLimpiarFiltros,
  totalPagos,
  pagosFiltrados
}) => {
  const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8099';
  const [mediosPago, setMediosPago] = useState([]);

  useEffect(() => {
    // Pedir todos los medios de pago (o un número grande) para llenar el select
    fetch(`${BACKEND}/api/medio-pagos/?per_page=100`)
      .then(r => r.json())
      .then(j => { if (j.status === 'success') setMediosPago(j.data) })
      .catch(err => console.error('Error cargando medios de pago:', err));
  }, []);

  return (
    <div className="mb-4 p-3 bg-light rounded"> 
      <h5 className="mb-3">🔍 Filtros de Búsqueda</h5> 
      <Row className="mb-3">
        <Col md={6}>
          <InputGroup>
            <InputGroup.Text>🔎</InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Buscar por código de factura..."
              value={busqueda}
              onChange={(e) => onBusquedaChange(e.target.value)}
            />
          </InputGroup>
        </Col>
      </Row>
      <Row>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Fecha Desde</Form.Label>
            <Form.Control
              type="date"
              value={filtros.fecha_desde || ''}
              onChange={(e) => onFiltroChange('fecha_desde', e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Fecha Hasta</Form.Label>
            <Form.Control
              type="date"
              value={filtros.fecha_hasta || ''}
              onChange={(e) => onFiltroChange('fecha_hasta', e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Medio de Pago</Form.Label>
            <Form.Select
              value={filtros.id_medio_pago || ''}
              onChange={(e) => onFiltroChange('id_medio_pago', e.target.value)}
            >
              <option value="">Todos</option>
              {mediosPago
                .filter(mp => !mp.baja)
                .map((mp) => (
                  <option key={mp.id_medio_pago} value={mp.id_medio_pago}>
                    {mp.nombre}
                  </option>
                ))}
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col className="d-flex align-items-center gap-2">
          <Button variant="secondary" onClick={onLimpiarFiltros}>
            Limpiar Filtros
          </Button>
          <Badge bg="info">
            {pagosFiltrados} de {totalPagos} pagos
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosPagos;

