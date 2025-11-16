import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosProductos = ({
  filtros,
  onFiltroChange,
  busqueda,
  onBusquedaChange,
  onLimpiar,
  secciones,
  totalProductos,
  productosFiltrados
}) => {
  return (
    <div className="mb-4 p-3 bg-light rounded">
      <h5 className="mb-3">🛒 Filtros de Productos</h5>

      {/* Búsqueda por nombre o código */}
      <Row className="mb-3">
        <Col md={6}>
          <InputGroup>
            <InputGroup.Text>🔎</InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Buscar por nombre o código..."
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
              value={filtros.activos}
              onChange={(e) => onFiltroChange('activos', e.target.value)}
            >
              <option value="">Todos</option>
              <option value="true">Activos</option>
              <option value="false">Dados de baja</option>
            </Form.Select>
          </Form.Group>
        </Col>

        {/* Sección */}
        <Col md={3}>
          <Form.Group>
            <Form.Label>Sección</Form.Label>
            <Form.Select
              value={filtros.id_seccion}
              onChange={(e) => onFiltroChange('id_seccion', e.target.value)}
            >
              <option value="">Todas las secciones</option>
              {secciones
                .filter(s => !s.baja)
                .map((seccion) => (
                  <option key={seccion.id_seccion} value={seccion.id_seccion}>
                    {seccion.nombre}
                  </option>
                ))}
            </Form.Select>
          </Form.Group>
        </Col>

        {/* Precio mínimo */}
        <Col md={3}>
          <Form.Group>
            <Form.Label>Precio mínimo</Form.Label>
            <Form.Control
              type="number"
              min="0"
              step="0.01"
              value={filtros.precioMin}
              onChange={(e) => onFiltroChange('precioMin', e.target.value)}
              placeholder="Ej: 100.00"
            />
          </Form.Group>
        </Col>

        {/* Precio máximo */}
        <Col md={3}>
          <Form.Group>
            <Form.Label>Precio máximo</Form.Label>
            <Form.Control
              type="number"
              min="0"
              step="0.01"
              value={filtros.precioMax}
              onChange={(e) => onFiltroChange('precioMax', e.target.value)}
              placeholder="Ej: 500.00"
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
            {productosFiltrados} de {totalProductos} productos
          </Badge>
        </Col>
      </Row>
    </div>
  );
};

export default FiltrosProductos;
