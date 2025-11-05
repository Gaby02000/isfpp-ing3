import React from 'react';
import { Pagination } from 'react-bootstrap';

const Paginacion = ({ 
  currentPage, 
  totalPages, 
  onPageChange,
  hasNext,
  hasPrev 
}) => {
  if (totalPages <= 1) {
    return null;
  }

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages && page !== currentPage) {
      onPageChange(page);
    }
  };

  // Generar números de página a mostrar
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;
    
    if (totalPages <= maxVisible) {
      // Mostrar todas las páginas si hay pocas
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Mostrar páginas alrededor de la actual
      let start = Math.max(1, currentPage - 2);
      let end = Math.min(totalPages, currentPage + 2);
      
      if (currentPage <= 3) {
        end = Math.min(maxVisible, totalPages);
      } else if (currentPage >= totalPages - 2) {
        start = Math.max(1, totalPages - maxVisible + 1);
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
    }
    
    return pages;
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="d-flex justify-content-center mt-4">
      <Pagination>
        <Pagination.First 
          disabled={!hasPrev} 
          onClick={() => handlePageChange(1)} 
        />
        <Pagination.Prev 
          disabled={!hasPrev} 
          onClick={() => handlePageChange(currentPage - 1)} 
        />
        
        {pageNumbers[0] > 1 && (
          <>
            <Pagination.Item onClick={() => handlePageChange(1)}>
              {1}
            </Pagination.Item>
            {pageNumbers[0] > 2 && <Pagination.Ellipsis />}
          </>
        )}
        
        {pageNumbers.map((page) => (
          <Pagination.Item
            key={page}
            active={page === currentPage}
            onClick={() => handlePageChange(page)}
          >
            {page}
          </Pagination.Item>
        ))}
        
        {pageNumbers[pageNumbers.length - 1] < totalPages && (
          <>
            {pageNumbers[pageNumbers.length - 1] < totalPages - 1 && (
              <Pagination.Ellipsis />
            )}
            <Pagination.Item onClick={() => handlePageChange(totalPages)}>
              {totalPages}
            </Pagination.Item>
          </>
        )}
        
        <Pagination.Next 
          disabled={!hasNext} 
          onClick={() => handlePageChange(currentPage + 1)} 
        />
        <Pagination.Last 
          disabled={!hasNext} 
          onClick={() => handlePageChange(totalPages)} 
        />
      </Pagination>
    </div>
  );
};

export default Paginacion;

