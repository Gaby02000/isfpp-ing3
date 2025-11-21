import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosReserva = ({
  filtros,
  onFiltroChange,
  busqueda,
  onBusquedaChange,
  onLimpiar,
  clientes,
  totalReservas,
  reservasFiltradas
}) => {
  return (
    <div className="mb-4 p-3 bg-light rounded">
      <h5 className="mb-3">📅 Filtros de Reservas</h5>

      {/* Búsqueda por número de reserva */}
      <Row className="mb-3">
        <Col md={6}>
          <InputGroup>
            <InputGroup.Text>🔎</InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Buscar por número de reserva..."
              value={busqueda}
              onChange={(e) => onBusquedaChange(e.target.value)}
            />
          </InputGroup>
        </Col>
      </Row>

      {/* Filtros principales */}
      <Row>
        {/* Estado */}
        <Col md={3}>
          <Form.Group>
            <Form.Label>Estado</Form.Label>
            <Form.Select
              value={filtros.cancelado}
              onChange={(e) => onFiltroChange('cancelado', e.target.value)}
            >
              <option value="">Todos</option>
              <option value="activo">Activos</option>
              <option value="cancelado">Estados</option>
            </Form.Select>
          </Form.Group>
        </Col>

        {/* Cliente */}
        <Col md={3}>
          <Form.Group>
            <Form.Label>Cliente</Form.Label>
            <Form.Select
              value={filtros.cliente_id || ''}   // 👈 fallback a string vacío
              onChange={(e) => onFiltroChange('cliente_id', e.target.value)}
            >
              <option value="">Todos los clientes</option>   {/* 👈 opción inicial */}
              {clientes
                .filter(c => !c.baja)
                .map((cliente) => (
                  <option key={cliente.id_cliente} value={cliente.id_cliente}>
                    {cliente.nombre} {cliente.apellido}
                  </option>
                ))}
            </Form.Select>
          </Form.Group>
        </Col>
        {/* Fecha desde */}
        <Col md={3}>
          <Form.Group>
            <Form.Label>Fecha desde</Form.Label>
            <Form.Control
              type="date"
              value={filtros.fecha_desde || ''}
              onChange={(e) => onFiltroChange('fecha_desde', e.target.value)}
            />
          </Form.Group>
        </Col>

        {/* Fecha hasta */}
        <Col md={3}>
          <Form.Group>
            <Form.Label>Fecha hasta</Form.Label>
            <Form.Control
              type="date"
              value={filtros.fecha_hasta || ''}
              onChange={(e) => onFiltroChange('fecha_hasta', e.target.value)}
            />
          </Form.Group>
        </Col>
      </Row>

      {/* Botón limpiar y conteo */}
      <Row className="mt-3">
        <Col>
          <Button variant="outline-secondary" size="sm" onClick={onLimpiar}>
            Limpiar Filtros
          </Button>
          <Badge bg="info" className="ms-2">
            {reservasFiltradas} de {totalReservas} reservas
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosReserva;