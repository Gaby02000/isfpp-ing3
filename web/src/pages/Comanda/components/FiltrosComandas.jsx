import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosComandas = ({ 
  filtros, 
  onFiltroChange,
  busqueda,
  onBusquedaChange,
  onLimpiarFiltros,
  mesas,
  mozos,
  totalComandas,
  comandasFiltradas
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
              placeholder="Buscar por número de comanda o mesa..."
              value={busqueda}
              onChange={(e) => onBusquedaChange(e.target.value)}
            />
          </InputGroup>
        </Col>
      </Row>
      <Row>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Fecha</Form.Label>
            <Form.Control
              type="date"
              value={filtros.fecha}
              onChange={(e) => onFiltroChange('fecha', e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Mesa</Form.Label>
            <Form.Select
              value={filtros.id_mesa}
              onChange={(e) => onFiltroChange('id_mesa', e.target.value)}
            >
              <option value="">Todas las mesas</option>
              {mesas
                .filter(mesa => !mesa.baja)
                .map((mesa) => (
                  <option key={mesa.id_mesa} value={mesa.id_mesa}>
                    Mesa {mesa.numero}
                  </option>
                ))}
            </Form.Select>
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group>
            <Form.Label>Mozo</Form.Label>
            <Form.Select
              value={filtros.id_mozo}
              onChange={(e) => onFiltroChange('id_mozo', e.target.value)}
            >
              <option value="">Todos los mozos</option>
              {mozos
                .filter(mozo => !mozo.baja)
                .map((mozo) => (
                  <option key={mozo.id} value={mozo.id}>
                    {mozo.nombre_apellido}
                  </option>
                ))}
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
              <option value="abierta">Abierta</option>
              <option value="cerrada">Cerrada</option>
              <option value="baja">Cancelada</option>
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
            {comandasFiltradas} de {totalComandas} comandas
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosComandas;