import React from 'react';
import { Container } from 'react-bootstrap';
import NavigationBar from './NavigationBar';

const Layout = ({ children }) => {
  return (
    <>
      <NavigationBar />
      <Container>
        {children}
      </Container>
    </>
  );
};

export default Layout;