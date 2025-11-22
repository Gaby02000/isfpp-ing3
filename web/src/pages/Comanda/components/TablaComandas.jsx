import React from 'react';
import { Table, Button, Badge } from 'react-bootstrap';

const TablaComandas = ({ comandas, onEdit, onDelete }) => {
  if (comandas.length === 0) {
    return (    
        <Table striped bordered hover responsive>
            <thead>
                <tr>
                    <th>Número de Comanda</th>
                    <th>Número de Mesa</th>
                    <th>Mozo</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>    
            <tbody>
                <tr>
                    <td colSpan="5" className="text-center text-muted">
                        No hay comandas registradas
                    </td>
                </tr>
            </tbody>
        </Table>
    );
  }
    return (
    <Table striped bordered hover responsive>
      <thead>
        <tr>
            <th>N° Comanda</th>
            <th>N° Mesa</th>
            <th>Mozo</th>
            <th>Estado</th>
            <th>Acciones</th>
        </tr>
      </thead>
        <tbody>
        {comandas.map((comanda) => (
    <tr key={comanda.id_comanda}>
      <td>
        <Badge bg="info">#{comanda.id_comanda}</Badge>
      </td>
      <td>{comanda.mesa ? (
        <Badge bg="info">Mesa {comanda.mesa.numero}</Badge>
      ) : (
        <span className="text-muted">-</span>
      )}</td>
      <td>{comanda.mozo ? (
        <span>{comanda.mozo.nombre_apellido}</span>
      ) : (   
        <span className="text-muted">-</span>
      )}</td>
      <td>
        <Badge bg={comanda.baja ? 'danger' : 'success'}>
          {comanda.baja ? 'Inactiva' : 'Activa'}
        </Badge>
      </td>
                <td>
                    <Button
                        variant="primary"
                        size ="sm"
                        className="me-2"
                        onClick={() => onEdit(comanda)}
                        disabled={comanda.baja}
                    >
                        Editar      
                    </Button>
                    <Button
                        variant="danger"
                        size="sm"
                        onClick={() => onDelete(comanda)}
                        disabled={comanda.baja}
                    >
                        Dar de Baja
                    </Button>
                </td>
            </tr>
        ))}
        </tbody>
    </Table>
  );
};

export default TablaComandas;
                
                