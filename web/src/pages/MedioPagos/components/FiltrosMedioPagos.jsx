import React from 'react';  
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosMedioPagos = ({
    filtros,
    onFiltroChange,
    busqueda,
    onBusquedaChange,
    onLimpiar,
    totalMediosPagos,
    mediosPagosFiltrados
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
                            placeholder="Buscar por nombre"
                            value={busqueda}
                            onChange={(e) => onBusquedaChange(e.target.value)}
                        />
                    </InputGroup>
                </Col>
            </Row>
            <Row>
                <Col md={4}>
                    <Form.Group>
                        <Form.Label>Nombre del Medio de Pago</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Ej: Efectivo, Tarjeta..."
                            value={filtros.nombre}
                            onChange={(e) => onFiltroChange('nombre', e.target.value)}
                        />
                    </Form.Group>
                </Col>
                <Col md={3}>
                    <Form.Group>
                        <Form.Label>Estado</Form.Label>
                        <Form.Select
                            value={filtros.estado}
                            onChange={(e) => onFiltroChange('estado', e.target.value)}
                        >
                            <option value="">Todos los estados</option>
                            <option value="activa">Activo</option>
                            <option value="baja">Inactivo</option>
                        </Form.Select>
                    </Form.Group>
                </Col>
            </Row>
            <Row className="mt-2">
                    <Col>
                      <Button variant="outline-secondary" size="sm" onClick={onLimpiar}>
                        Limpiar Filtros
                      </Button>
                      {mediosPagosFiltrados !== undefined && totalMediosPagos !== undefined && (
                        <Badge bg="info" className="ms-2">
                          {mediosPagosFiltrados} de {totalMediosPagos} medios de pago
                        </Badge>
                      )}
                    </Col>
                  </Row>
                </div>
                );
};

export default FiltrosMedioPagos;