import React from 'react';
import { Row, Col, Form, InputGroup, Button, Badge } from 'react-bootstrap';

const FiltrosComandas = ({ 
  filtros, 
  onFiltroChange,
    busqueda,
    onBusquedaChange,
    onLimpiar,
    mesa,
    mozo,
    estadosComanda,
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
                        placeholder="Buscar por numero..."
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
                        value={filtros.mesa_numero}
                        onChange={(e) => onFiltroChange('mesa_numero', e.target.value)}
                    />
                </Form.Group>
            </Col>
            <Col md={3}>
                <Form.Group>
                    <Form.Label>Mozo</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Nombre del mozo..."
                        value={filtros.mozo_nombre}
                        onChange={(e) => onFiltroChange('mozo_nombre', e.target.value)}
                    />
                </Form.Group>
            </Col>
            <Col md={3}>
                <Form.Group>
                    <Form.Label>Estado de Comanda</Form.Label>
                    <Form.Select
                        value={filtros.estado}
                        onChange={(e) => onFiltroChange('estado', e.target.value)}
                    >
                        <option value="">Todos</option>
                        <option value="abierta">Abierta</option>
                        <option value ="baja">Bajada</option>
                        <option value="cerrada">Cerrada</option>
                        
                    </Form.Select>
                </Form.Group>
            </Col>
            <Col md={3} className="d-flex align-items-end">
                <Button variant="secondary" onClick={onLimpiar}>
                    Limpiar Filtros
                </Button>
                <Badge bg="info" className="ms-2">
                    {comandasFiltradas} de {totalComandas} comandas
                </Badge>
            </Col>  
        </Row>
    </div>
    );
};
export default FiltrosComandas;