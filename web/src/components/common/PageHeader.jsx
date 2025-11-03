import React from 'react';
import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const PageHeader = ({ title, backPath, backLabel = '← Volver', children }) => {
  const navigate = useNavigate();
  
  return (
    <div className="mb-4">
      {backPath && (
        <Button 
          variant="outline-secondary" 
          onClick={() => navigate(backPath)}
          className="me-3"
        >
          {backLabel}
        </Button>
      )}
      <h2 className="d-inline">{title}</h2>
      {children}
    </div>
  );
};

export default PageHeader;

