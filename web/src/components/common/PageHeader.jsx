import React from 'react';
import { Button, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const PageHeader = ({ 
  title, 
  backPath, 
  backLabel = '← Volver', 
  createButton,
  createLabel,
  onCreate,
  children 
}) => {
  const navigate = useNavigate();
  
  return (
    <div className="mb-4">
      <Row className="align-items-center">
        <Col xs="auto">
          {backPath && (
            <Button 
              variant="outline-secondary" 
              size="sm"
              onClick={() => navigate(backPath)}
              className="me-2"
            >
              {backLabel}
            </Button>
          )}
        </Col>
        <Col>
          <h1 className="h3 mb-0 fw-bold">{title}</h1>
        </Col>
        {(createButton || onCreate) && (
          <Col xs="auto">
            <Button 
              variant="primary" 
              onClick={onCreate}
              size="sm"
            >
              {createLabel || createButton || '+ Nuevo'}
            </Button>
          </Col>
        )}
        {children && (
          <Col xs="auto">
            {children}
          </Col>
        )}
      </Row>
    </div>
  );
};

export default PageHeader;

